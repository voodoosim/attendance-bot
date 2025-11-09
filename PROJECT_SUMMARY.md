# 출석 봇 (Attendance Bot) - 프로젝트 요약

> **개발 완료일**: 2025-11-09
> **상태**: ✅ 배포 준비 완료
> **Repository**: https://github.com/voodoosim/attendance-bot

---

## 📋 프로젝트 개요

Telegram 기반 출석 체크 및 채팅 활동 보상 봇으로, Clean Architecture를 적용한 현대적인 설계를 갖추고 있습니다.

### 핵심 기능

1. **출석 시스템** (`/출첵`)
   - 일일 출석으로 10점 + 연속 출석 보너스 (최대 +7점)
   - 신규 유저 자동 등록
   - 연속 출석일 자동 계산

2. **채팅 보상 시스템**
   - 메시지당 랜덤 1~6점 자동 지급
   - 5% 확률 잭팟 (1~7배 배율 적용)
   - 조용한 보상 (잭팟만 알림)

3. **랭킹 시스템** (4종)
   - `/랭킹` - 점수 순위 TOP 10
   - `/채팅랭킹` - 채팅 수 순위
   - `/잭팟랭킹` - 잭팟 횟수 순위
   - `/출석랭킹` - 연속 출석 순위

4. **통계 시스템** (2종)
   - `/일일통계` - 오늘의 활동 통계
   - `/월통계` - 이번 달 통계

---

## 🏗️ 기술 스택 및 아키텍처

### Architecture
- **패턴**: Clean Architecture (5-Layer)
- **Layer 구조**:
  ```
  Layer 1: Core (Entities + Use Cases)
  Layer 2: Services (Business Logic)
  Layer 3: Repositories (Data Access)
  Layer 4: Handlers (Presentation)
  Layer 5: Infrastructure (Database, External)
  ```

### 기술 스택
- **Framework**: aiogram 3.13.1 (비동기 Telegram Bot)
- **ORM**: SQLAlchemy 2.0 (Async)
- **Database**: PostgreSQL (운영) / SQLite (개발)
- **Migration**: Alembic
- **Validation**: Pydantic 2.0
- **Container**: Docker + Docker Compose

---

## 📊 프로젝트 통계

```
총 Python 파일: 38개
총 코드 라인: 2,052줄
핸들러: 6개
명령어: 10개
데이터베이스 테이블: 4개
Repository: 4개
Use Case: 6개
Service: 4개
Entity: 5개
```

---

## 🔧 Git 커밋 히스토리

### Commit 1: 초기 설정 (1032fe2)
```
feat: initial project setup with Clean Architecture
- Clean Architecture 5-layer 구조
- 기본 설정 파일 (requirements.txt, config.py)
- GitHub 리포지토리 생성
```

### Commit 2: Core & Database (d89e9cb)
```
feat: implement core domain and database layer
- 4개 Core Entities (User, Attendance, ChatActivity, ScoreConfig)
- SQLAlchemy 비동기 모델
- Alembic 초기 마이그레이션
- 설계 문서 (REQUIREMENTS.md, DESIGN.md)
```

### Commit 3: 전체 구현 (e840726)
```
feat: implement complete attendance bot with gamification
- 4개 Repository (User, Attendance, ChatActivity, ScoreConfig)
- 4개 Use Cases (CheckIn, ProcessMessage, GetUserInfo, GetRanking)
- 3개 Services (Attendance, ChatActivity, User)
- 5개 Handlers (start, check_in, message, user_info, ranking)
- main.py 의존성 주입 설정
```

### Commit 4: Docker 배포 (1a65f3f)
```
feat: add Docker and VPS deployment support
- Dockerfile (Python 3.10)
- docker-compose.yml (PostgreSQL 15)
- deploy.sh 스크립트
- VPS 배포 가이드
```

### Commit 5: 한글화 (cd6df6f)
```
refactor: convert all commands to Korean
- /start → /시작
- 모든 명령어 한글 전용
- README 명령어 표 업데이트
```

### Commit 6: 통계 기능 (244c9a5)
```
feat: add daily and monthly statistics features
- /일일통계, /월통계 명령어
- Stats Entity (DailyStats, MonthlyStats)
- 2개 Use Cases (GetDailyStats, GetMonthlyStats)
- StatsService 및 stats_handler
- Repository 통계 쿼리 메서드
```

### Commit 7: SQLite 버그 수정 (3de6c14)
```
fix: resolve SQLite connection pool compatibility issue
- SQLite pool_size/max_overflow 오류 수정
- 조건부 pool 설정 (DB 타입별)
- 개발/운영 환경 모두 호환
```

---

## 📋 전체 명령어 목록 (10개)

| 명령어 | 설명 | 구현 상태 |
|--------|------|-----------|
| `/시작` | 봇 시작 및 안내 메시지 | ✅ |
| `/도움말` | 상세 사용 가이드 | ✅ |
| `/출첵` | 일일 출석 체크 (신규 등록) | ✅ |
| `/내정보` | 내 통계 및 출석 현황 조회 | ✅ |
| `/랭킹` | 점수 순위 TOP 10 | ✅ |
| `/채팅랭킹` | 채팅 수 순위 TOP 10 | ✅ |
| `/잭팟랭킹` | 잭팟 횟수 순위 TOP 10 | ✅ |
| `/출석랭킹` | 연속 출석일 순위 TOP 10 | ✅ |
| `/일일통계` | 오늘의 활동 통계 | ✅ |
| `/월통계` | 이번 달 통계 | ✅ |

---

## 🗂️ 디렉토리 구조

```
attendance-bot/
├── src/
│   ├── core/                      # Layer 1: Domain
│   │   ├── entities/              # 5개 Entity
│   │   │   ├── user.py
│   │   │   ├── attendance.py
│   │   │   ├── chat_activity.py
│   │   │   ├── score_config.py
│   │   │   └── stats.py
│   │   └── use_cases/             # 6개 Use Case
│   │       ├── check_in_usecase.py
│   │       ├── process_message_usecase.py
│   │       ├── get_user_info_usecase.py
│   │       ├── get_ranking_usecase.py
│   │       ├── get_daily_stats_usecase.py
│   │       └── get_monthly_stats_usecase.py
│   ├── services/                  # Layer 2: Services
│   │   ├── attendance_service.py
│   │   ├── chat_activity_service.py
│   │   ├── user_service.py
│   │   └── stats_service.py
│   ├── repositories/              # Layer 3: Data Access
│   │   ├── user_repository.py
│   │   ├── attendance_repository.py
│   │   ├── chat_activity_repository.py
│   │   └── score_config_repository.py
│   ├── handlers/                  # Layer 4: Presentation
│   │   ├── start_handler.py
│   │   ├── check_in_handler.py
│   │   ├── message_handler.py
│   │   ├── user_info_handler.py
│   │   ├── ranking_handler.py
│   │   └── stats_handler.py
│   └── infrastructure/            # Layer 5: Infrastructure
│       └── database/
│           ├── connection.py
│           └── models.py
├── alembic/                       # Database Migration
│   └── versions/
│       └── 53cb0434c044_initial_migration_create_tables.py
├── docs/                          # Documentation
│   ├── REQUIREMENTS.md
│   └── DESIGN.md
├── config.py                      # Settings
├── main.py                        # Entry Point
├── requirements.txt               # Dependencies
├── Dockerfile                     # Docker Image
├── docker-compose.yml             # Docker Services
├── deploy.sh                      # Deployment Script
└── README.md                      # Main Documentation
```

---

## 🔍 검증 완료 항목

### ✅ 코드 품질 검증
1. **Python 문법**: 모든 파일 문법 오류 없음
2. **Import 체크**: 54개 컴포넌트 순환 참조 없음
3. **SQLAlchemy 쿼리**: 모든 쿼리 구문 검증 완료
4. **비즈니스 로직**: UseCase 로직 검증 완료
5. **통합 테스트**: Handler 라우터 등록 확인

### ✅ 발견 및 수정된 버그
- **SQLite Connection Pool 오류**: 수정 완료 (commit 3de6c14)

### ✅ 배포 준비
- Docker 설정 완료
- PostgreSQL 호환성 확인
- VPS 배포 스크립트 준비
- 환경 변수 설정 가이드

---

## 🚀 배포 방법

### 로컬 개발 환경
```bash
# 1. 환경 변수 설정
cp .env.example .env
nano .env  # BOT_TOKEN 입력

# 2. 가상환경 설정
python -m venv venv
source venv/bin/activate

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 데이터베이스 마이그레이션
alembic upgrade head

# 5. 봇 실행
python main.py
```

### VPS 배포 (Docker)
```bash
# 1. 저장소 클론
git clone https://github.com/voodoosim/attendance-bot.git
cd attendance-bot

# 2. 환경 변수 설정
cp .env.example .env
nano .env  # BOT_TOKEN 입력

# 3. 봇 시작
./deploy.sh start

# 4. 로그 확인
./deploy.sh logs
```

---

## 📝 환경 변수 (.env)

```bash
# 필수
BOT_TOKEN=your_bot_token_here

# PostgreSQL (운영)
DATABASE_URL=postgresql+asyncpg://attendance_user:attendance_pass@postgres:5432/attendance_db

# SQLite (개발)
# DATABASE_URL=sqlite+aiosqlite:///./attendance.db

# 선택
ADMIN_IDS=123456789
TIMEZONE=Asia/Seoul
DEBUG=False
LOG_LEVEL=INFO
```

---

## 🎯 주요 설계 결정

### 1. Clean Architecture 채택
- **이유**: 유지보수성, 테스트 용이성, 확장성
- **결과**: 계층별 명확한 책임 분리

### 2. 비동기 아키텍처
- **이유**: Telegram Bot의 동시 요청 처리
- **기술**: aiogram 3.x + SQLAlchemy 2.0 Async

### 3. 의존성 주입 (DI)
- **방식**: aiogram Middleware 기반
- **효과**: 테스트 가능성 향상, 결합도 감소

### 4. Repository 패턴
- **목적**: 데이터 접근 로직 추상화
- **장점**: ORM 교체 용이, 비즈니스 로직 분리

### 5. Docker 컨테이너화
- **이유**: 일관된 개발/운영 환경
- **구성**: Bot + PostgreSQL + Alembic Migration

---

## 🐛 알려진 제한사항

1. **통계 TOP 사용자**
   - 현재: 전체 누적 랭킹 표시
   - 개선 가능: 일일/월별 TOP 사용자 필터링

2. **테스트 코드**
   - 현재: 미구현
   - 향후: pytest + pytest-asyncio 추가 예정

---

## 📚 참고 문서

- **설계 문서**: `docs/DESIGN.md`
- **요구사항**: `docs/REQUIREMENTS.md`
- **배포 가이드**: `README.md`
- **API 문서**: 각 모듈의 docstring 참조

---

## 👥 기여자

- **Developer**: Sasori ([@voodoosim](https://github.com/voodoosim))
- **AI Assistant**: Claude Code (Anthropic)

---

## 📄 라이선스

MIT License - `LICENSE` 파일 참조

---

**마지막 업데이트**: 2025-11-09
**프로젝트 상태**: ✅ 배포 준비 완료
