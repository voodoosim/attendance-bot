# 🏗️ 출석 봇 설계 문서

> **작성일**: 2025-11-09
> **버전**: 1.0.0
> **아키텍처**: Clean Architecture (5-layer)

---

## 📐 시스템 아키텍처

### Clean Architecture 레이어

```
┌─────────────────────────────────────────────────────┐
│                  Layer 5: Handlers                  │
│            (Telegram Bot Message Handlers)          │
│  - CheckInHandler (.출첵)                           │
│  - MessageHandler (채팅 활동)                       │
│  - InfoHandler (.내정보)                            │
│  - RankingHandler (.랭킹)                           │
└─────────────────────────────────────────────────────┘
                        ▼ depends on
┌─────────────────────────────────────────────────────┐
│                  Layer 4: Services                  │
│              (Business Logic Services)              │
│  - AttendanceService (출석 로직)                    │
│  - ChatActivityService (채팅 보상 로직)             │
│  - ScoreService (점수 계산)                         │
│  - RankingService (랭킹 조회)                       │
└─────────────────────────────────────────────────────┘
                        ▼ depends on
┌─────────────────────────────────────────────────────┐
│                 Layer 3: Repositories               │
│                (Data Access Layer)                  │
│  - UserRepository                                   │
│  - AttendanceRepository                             │
│  - ChatActivityRepository                           │
│  - ScoreConfigRepository                            │
└─────────────────────────────────────────────────────┘
                        ▼ depends on
┌─────────────────────────────────────────────────────┐
│              Layer 2: Core / Use Cases              │
│                  (Domain Logic)                     │
│  - Entities: User, Attendance, ChatActivity         │
│  - Use Cases: CheckIn, ProcessMessage, GetRanking   │
└─────────────────────────────────────────────────────┘
                        ▼ depends on
┌─────────────────────────────────────────────────────┐
│                Layer 1: Infrastructure              │
│           (Database, External Services)             │
│  - Database Models (SQLAlchemy)                     │
│  - Database Connection                              │
│  - Configuration                                    │
└─────────────────────────────────────────────────────┘
```

---

## 🎯 핵심 컴포넌트

### 1. Entities (도메인 엔티티)

#### User Entity
```python
@dataclass
class User:
    """사용자 도메인 엔티티"""
    id: int
    telegram_id: int
    username: str
    total_score: int
    chat_count: int
    jackpot_count: int
    max_jackpot: int
    consecutive_days: int
    total_attendance: int
    last_checkin: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    def can_checkin_today(self) -> bool:
        """오늘 출석 가능 여부"""
        if not self.last_checkin:
            return True
        return self.last_checkin.date() < datetime.now().date()

    def calculate_consecutive_days(self) -> int:
        """연속 출석일 계산"""
        if not self.last_checkin:
            return 1
        days_diff = (datetime.now().date() - self.last_checkin.date()).days
        if days_diff == 1:
            return self.consecutive_days + 1
        return 1  # 연속 끊김

    def add_score(self, score: int):
        """점수 추가"""
        self.total_score += score

    def increment_chat_count(self):
        """채팅 수 증가"""
        self.chat_count += 1
```

#### Attendance Entity
```python
@dataclass
class Attendance:
    """출석 기록 엔티티"""
    id: int
    user_id: int
    date: date
    score: int
    consecutive_days: int
    created_at: datetime
```

#### ChatActivity Entity
```python
@dataclass
class ChatActivity:
    """채팅 활동 엔티티"""
    id: int
    user_id: int
    message_id: int
    base_score: int
    is_jackpot: bool
    multiplier: int
    final_score: int
    created_at: datetime

    @staticmethod
    def create_activity(
        user_id: int,
        message_id: int,
        config: 'ScoreConfig'
    ) -> 'ChatActivity':
        """채팅 활동 생성 (점수 계산 포함)"""
        base_score = random.randint(config.chat_score_min, config.chat_score_max)
        is_jackpot = random.random() < config.jackpot_chance

        if is_jackpot:
            multiplier = random.randint(config.multiplier_min, config.multiplier_max)
            final_score = base_score * multiplier
        else:
            multiplier = 1
            final_score = base_score

        return ChatActivity(
            id=0,  # DB에서 할당
            user_id=user_id,
            message_id=message_id,
            base_score=base_score,
            is_jackpot=is_jackpot,
            multiplier=multiplier,
            final_score=final_score,
            created_at=datetime.now()
        )
```

#### ScoreConfig Entity
```python
@dataclass
class ScoreConfig:
    """점수 설정 엔티티"""
    id: int
    attendance_score: int = 10
    chat_score_min: int = 1
    chat_score_max: int = 6
    jackpot_chance: float = 0.05  # 5%
    multiplier_min: int = 1
    multiplier_max: int = 7
    max_consecutive_bonus: int = 7
    updated_at: datetime = None
```

---

### 2. Use Cases (유스케이스)

#### CheckInUseCase
```python
class CheckInUseCase:
    """출석 체크 유스케이스"""

    def __init__(
        self,
        user_repo: UserRepository,
        attendance_repo: AttendanceRepository,
        config_repo: ScoreConfigRepository
    ):
        self.user_repo = user_repo
        self.attendance_repo = attendance_repo
        self.config_repo = config_repo

    async def execute(self, telegram_id: int, username: str) -> CheckInResult:
        """출석 체크 실행"""
        # 1. 사용자 조회 또는 생성
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user:
            user = await self.user_repo.create(telegram_id, username)

        # 2. 오늘 출석 가능 여부 확인
        if not user.can_checkin_today():
            raise AlreadyCheckedInError("이미 오늘 출석했습니다")

        # 3. 연속 출석일 계산
        consecutive_days = user.calculate_consecutive_days()

        # 4. 출석 점수 계산
        config = await self.config_repo.get_config()
        bonus = min(consecutive_days, config.max_consecutive_bonus)
        score = config.attendance_score + bonus

        # 5. 출석 기록 저장
        attendance = await self.attendance_repo.create(
            user_id=user.id,
            date=datetime.now().date(),
            score=score,
            consecutive_days=consecutive_days
        )

        # 6. 사용자 정보 업데이트
        user.consecutive_days = consecutive_days
        user.total_attendance += 1
        user.total_score += score
        user.last_checkin = datetime.now()
        await self.user_repo.update(user)

        return CheckInResult(
            user=user,
            score=score,
            consecutive_days=consecutive_days
        )
```

#### ProcessMessageUseCase
```python
class ProcessMessageUseCase:
    """메시지 처리 유스케이스"""

    def __init__(
        self,
        user_repo: UserRepository,
        chat_activity_repo: ChatActivityRepository,
        config_repo: ScoreConfigRepository
    ):
        self.user_repo = user_repo
        self.chat_activity_repo = chat_activity_repo
        self.config_repo = config_repo

    async def execute(
        self,
        telegram_id: int,
        message_id: int
    ) -> Optional[ProcessMessageResult]:
        """메시지 처리 및 점수 부여"""
        # 1. 등록된 사용자인지 확인
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user:
            return None  # 미등록 유저는 무시

        # 2. 점수 설정 조회
        config = await self.config_repo.get_config()

        # 3. 채팅 활동 생성 (점수 계산 포함)
        activity = ChatActivity.create_activity(
            user_id=user.id,
            message_id=message_id,
            config=config
        )

        # 4. 채팅 활동 저장
        await self.chat_activity_repo.create(activity)

        # 5. 사용자 정보 업데이트
        user.add_score(activity.final_score)
        user.increment_chat_count()

        if activity.is_jackpot:
            user.jackpot_count += 1
            if activity.final_score > user.max_jackpot:
                user.max_jackpot = activity.final_score

        await self.user_repo.update(user)

        return ProcessMessageResult(
            user=user,
            activity=activity
        )
```

---

### 3. Services (비즈니스 로직)

#### AttendanceService
```python
class AttendanceService:
    """출석 관련 서비스"""

    def __init__(self, checkin_usecase: CheckInUseCase):
        self.checkin_usecase = checkin_usecase

    async def check_in(
        self,
        telegram_id: int,
        username: str
    ) -> Dict[str, Any]:
        """출석 체크 처리"""
        try:
            result = await self.checkin_usecase.execute(telegram_id, username)
            return {
                "success": True,
                "user": result.user,
                "score": result.score,
                "consecutive_days": result.consecutive_days
            }
        except AlreadyCheckedInError as e:
            return {
                "success": False,
                "error": str(e)
            }
```

#### ChatActivityService
```python
class ChatActivityService:
    """채팅 활동 서비스"""

    def __init__(self, process_message_usecase: ProcessMessageUseCase):
        self.process_message_usecase = process_message_usecase

    async def process_message(
        self,
        telegram_id: int,
        message_id: int
    ) -> Optional[Dict[str, Any]]:
        """메시지 처리 및 점수 부여"""
        result = await self.process_message_usecase.execute(
            telegram_id,
            message_id
        )

        if not result:
            return None  # 미등록 유저

        return {
            "user": result.user,
            "activity": result.activity,
            "is_jackpot": result.activity.is_jackpot
        }
```

---

### 4. Repositories (데이터 접근)

#### UserRepository
```python
class UserRepository:
    """사용자 저장소"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Telegram ID로 사용자 조회"""
        pass

    async def create(self, telegram_id: int, username: str) -> User:
        """사용자 생성"""
        pass

    async def update(self, user: User) -> User:
        """사용자 업데이트"""
        pass

    async def get_ranking_by_score(self, limit: int = 10) -> List[User]:
        """점수 순위 조회"""
        pass

    async def get_ranking_by_chat_count(self, limit: int = 10) -> List[User]:
        """채팅 수 순위 조회"""
        pass
```

---

### 5. Handlers (텔레그램 핸들러)

#### CheckInHandler
```python
@router.message(Command("출첵"))
async def check_in_handler(message: Message, service: AttendanceService):
    """출석 체크 핸들러"""
    result = await service.check_in(
        telegram_id=message.from_user.id,
        username=message.from_user.username or "Unknown"
    )

    if result["success"]:
        user = result["user"]
        await message.reply(
            f"✅ 출석 체크 완료!\n"
            f"📅 연속 출석: {result['consecutive_days']}일\n"
            f"🎁 획득 점수: {result['score']}점\n"
            f"💰 총 점수: {user.total_score:,}점\n"
            f"💬 총 채팅 수: {user.chat_count:,}개"
        )
    else:
        await message.reply(f"❌ {result['error']}")
```

#### MessageHandler
```python
@router.message(F.text & ~F.text.startswith("/") & ~F.text.startswith("."))
async def message_handler(message: Message, service: ChatActivityService):
    """일반 메시지 핸들러 (채팅 활동)"""
    result = await service.process_message(
        telegram_id=message.from_user.id,
        message_id=message.message_id
    )

    if not result:
        return  # 미등록 유저 무시

    # 잭팟인 경우만 알림
    if result["is_jackpot"]:
        activity = result["activity"]
        await message.reply(
            f"🎰 잭팟!! 🎰\n"
            f"기본 점수: {activity.base_score}점\n"
            f"배율: x{activity.multiplier}\n"
            f"획득 점수: {activity.final_score}점!\n"
            f"💰 총 점수: {result['user'].total_score:,}점"
        )
```

---

## 🗄️ 데이터베이스 스키마

### users 테이블
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(255),
    total_score INTEGER DEFAULT 0,
    chat_count INTEGER DEFAULT 0,
    jackpot_count INTEGER DEFAULT 0,
    max_jackpot INTEGER DEFAULT 0,
    consecutive_days INTEGER DEFAULT 0,
    total_attendance INTEGER DEFAULT 0,
    last_checkin TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_telegram_id ON users(telegram_id);
CREATE INDEX idx_users_total_score ON users(total_score DESC);
CREATE INDEX idx_users_chat_count ON users(chat_count DESC);
```

### attendances 테이블
```sql
CREATE TABLE attendances (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    score INTEGER NOT NULL,
    consecutive_days INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, date)
);

CREATE INDEX idx_attendances_user_id ON attendances(user_id);
CREATE INDEX idx_attendances_date ON attendances(date DESC);
```

### chat_activities 테이블
```sql
CREATE TABLE chat_activities (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    message_id BIGINT NOT NULL,
    base_score INTEGER NOT NULL,
    is_jackpot BOOLEAN DEFAULT FALSE,
    multiplier INTEGER DEFAULT 1,
    final_score INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_chat_activities_user_id ON chat_activities(user_id);
CREATE INDEX idx_chat_activities_is_jackpot ON chat_activities(is_jackpot);
CREATE INDEX idx_chat_activities_created_at ON chat_activities(created_at DESC);
```

### score_configs 테이블
```sql
CREATE TABLE score_configs (
    id SERIAL PRIMARY KEY,
    attendance_score INTEGER DEFAULT 10,
    chat_score_min INTEGER DEFAULT 1,
    chat_score_max INTEGER DEFAULT 6,
    jackpot_chance FLOAT DEFAULT 0.05,
    multiplier_min INTEGER DEFAULT 1,
    multiplier_max INTEGER DEFAULT 7,
    max_consecutive_bonus INTEGER DEFAULT 7,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 기본 설정 데이터 삽입
INSERT INTO score_configs (id) VALUES (1);
```

---

## 🔄 데이터 흐름

### 출석 체크 흐름
```
User → .출첵 명령
    ↓
CheckInHandler
    ↓
AttendanceService
    ↓
CheckInUseCase
    ↓
UserRepository ← → Database
AttendanceRepository ← → Database
    ↓
Response to User
```

### 채팅 활동 흐름
```
User → 일반 메시지
    ↓
MessageHandler
    ↓
ChatActivityService
    ↓
ProcessMessageUseCase
    ↓
UserRepository ← → Database
ChatActivityRepository ← → Database
    ↓
(잭팟 시) Response to User
```

---

## 🧪 테스트 전략

### 1. Unit Tests
- Entity 로직 테스트 (점수 계산, 연속일 계산)
- Use Case 테스트 (mocked repositories)
- Service 테스트 (mocked use cases)

### 2. Integration Tests
- Repository 테스트 (실제 DB 연동)
- Handler 테스트 (mocked services)

### 3. E2E Tests
- 전체 플로우 테스트 (봇 → DB → 응답)

---

## 📦 의존성 주입

```python
# main.py
async def setup_dependencies(session: AsyncSession):
    # Repositories
    user_repo = UserRepository(session)
    attendance_repo = AttendanceRepository(session)
    chat_activity_repo = ChatActivityRepository(session)
    config_repo = ScoreConfigRepository(session)

    # Use Cases
    checkin_usecase = CheckInUseCase(user_repo, attendance_repo, config_repo)
    process_message_usecase = ProcessMessageUseCase(
        user_repo, chat_activity_repo, config_repo
    )

    # Services
    attendance_service = AttendanceService(checkin_usecase)
    chat_activity_service = ChatActivityService(process_message_usecase)

    return {
        "attendance_service": attendance_service,
        "chat_activity_service": chat_activity_service,
    }
```

---

**작성자**: Sasori
**승인 상태**: ✅ 승인됨
**다음 단계**: 구현 시작
