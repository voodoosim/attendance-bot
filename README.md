# 📝 Attendance Bot

> Telegram 출석 봇 - Clean Architecture를 적용한 현대적인 출석 관리 시스템

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![aiogram](https://img.shields.io/badge/aiogram-3.13.1-blue.svg)](https://github.com/aiogram/aiogram)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🎯 주요 기능

### 출석 시스템
- ✅ **출석 체크** (`/출첵`): 일일 출석으로 점수 획득
- ✅ **기본 점수**: 10점 + 연속 출석 보너스 (최대 +7점)
- ✅ **연속 출석**: 연속 출석일 자동 계산 및 보너스 적용

### 채팅 보상 시스템
- ✅ **랜덤 점수**: 메시지당 1~6점 랜덤 획득
- ✅ **잭팟 시스템**: 5% 확률로 1~7배 배율 적용
- ✅ **조용한 보상**: 일반 채팅은 조용히, 잭팟만 알림
- ✅ **등록 필수**: `/출첵` 등록자만 점수 획득

### 랭킹 시스템
- ✅ **점수 랭킹** (`/랭킹`): 총 점수 순위
- ✅ **채팅 랭킹** (`/채팅랭킹`): 채팅 수 순위
- ✅ **잭팟 랭킹** (`/잭팟랭킹`): 잭팟 횟수 순위
- ✅ **출석 랭킹** (`/출석랭킹`): 연속 출석일 순위

### 사용자 정보
- ✅ **내 정보** (`/내정보`): 개인 통계 및 기록 조회
- ✅ **출석 현황**: 최근 5일 출석 기록
- ✅ **잭팟 기록**: TOP 3 잭팟 기록 확인

## 🏗️ 아키텍처

Clean Architecture 5-layer 구조를 적용하여 유지보수성과 테스트 용이성을 극대화했습니다.

```
attendance-bot/
├── src/
│   ├── core/              # Layer 1: Core (Domain)
│   │   ├── entities/      # 도메인 엔티티
│   │   └── use_cases/     # 비즈니스 로직
│   ├── services/          # Layer 2: Services
│   ├── repositories/      # Layer 3: Data Access
│   ├── handlers/          # Layer 4: Presentation
│   └── infrastructure/    # Layer 5: Infrastructure
├── alembic/               # 데이터베이스 마이그레이션
├── tests/                 # 테스트 파일
├── config.py              # 설정 관리
└── main.py                # 진입점
```

## 🚀 빠른 시작

### 1. 사전 요구사항
- Python 3.10 이상
- PostgreSQL (프로덕션) 또는 SQLite (개발)
- Telegram Bot Token ([BotFather](https://t.me/botfather)에서 발급)

### 2. 설치

```bash
# 저장소 클론
git clone https://github.com/voodoosim/attendance-bot.git
cd attendance-bot

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 3. 환경 변수 설정

```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 편집
# BOT_TOKEN=your_bot_token_here
# ADMIN_IDS=123456789
# DATABASE_URL=sqlite+aiosqlite:///./attendance.db
```

### 4. 로컬 실행

```bash
# 데이터베이스 마이그레이션
alembic upgrade head

# 봇 실행
python main.py
```

## 🐳 VPS 배포 (Docker)

### 1. 서버 준비

```bash
# Docker 및 Docker Compose 설치 (Ubuntu)
sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker

# 사용자를 docker 그룹에 추가
sudo usermod -aG docker $USER
# 로그아웃 후 재로그인 필요
```

### 2. 프로젝트 배포

```bash
# 저장소 클론
git clone https://github.com/voodoosim/attendance-bot.git
cd attendance-bot

# 환경 변수 설정
cp .env.example .env
nano .env  # BOT_TOKEN 입력

# 봇 시작
./deploy.sh start
```

### 3. 배포 스크립트 사용법

```bash
./deploy.sh start    # 봇 시작
./deploy.sh stop     # 봇 중지
./deploy.sh restart  # 봇 재시작
./deploy.sh logs     # 로그 확인
./deploy.sh status   # 상태 확인
```

### 4. 환경 변수 설정 (.env)

```bash
# 필수 설정
BOT_TOKEN=your_bot_token_here
DATABASE_URL=postgresql+asyncpg://attendance_user:attendance_pass@postgres:5432/attendance_db

# 선택 설정
ADMIN_IDS=123456789,987654321
TIMEZONE=Asia/Seoul
DEBUG=False
LOG_LEVEL=INFO
```

### 5. 데이터 백업

```bash
# PostgreSQL 데이터 백업
docker exec attendance-postgres pg_dump -U attendance_user attendance_db > backup.sql

# 데이터 복원
docker exec -i attendance-postgres psql -U attendance_user attendance_db < backup.sql
```

## 📋 명령어 목록

### 사용자 명령어
| 명령어 | 설명 |
|--------|------|
| `/시작` | 봇 시작 및 안내 메시지 |
| `/도움말` | 상세 사용 가이드 |
| `/출첵` | 일일 출석 체크 (신규 등록) |
| `/내정보` | 내 통계 및 출석 현황 조회 |
| `/랭킹` | 점수 순위 TOP 10 |
| `/채팅랭킹` | 채팅 수 순위 TOP 10 |
| `/잭팟랭킹` | 잭팟 횟수 순위 TOP 10 |
| `/출석랭킹` | 연속 출석일 순위 TOP 10 |

## 🛠️ 기술 스택

- **Framework**: aiogram 3.13.1 (비동기 Telegram Bot 프레임워크)
- **Database**: SQLAlchemy 2.0 (ORM) + PostgreSQL/SQLite
- **Migration**: Alembic
- **Validation**: Pydantic 2.0
- **Testing**: pytest + pytest-asyncio
- **Code Quality**: black, flake8, mypy

## 📚 개발 가이드

### 개발 환경 설정

```bash
# 개발 의존성 설치
pip install -r requirements.txt

# 코드 포맷팅
black .

# 린트 체크
flake8 src

# 타입 체크
mypy src

# 테스트 실행
pytest
```

### 데이터베이스 마이그레이션

```bash
# 마이그레이션 생성
alembic revision --autogenerate -m "description"

# 마이그레이션 적용
alembic upgrade head

# 마이그레이션 롤백
alembic downgrade -1
```

## 🧪 테스트

```bash
# 전체 테스트 실행
pytest

# 커버리지 포함
pytest --cov=src --cov-report=html

# 특정 테스트만 실행
pytest tests/test_attendance.py
```

## ✅ 구현 완료

### Phase 1: 프로젝트 초기화
- [x] GitHub 리포지토리 생성
- [x] Clean Architecture 구조
- [x] 기본 설정 파일

### Phase 2: Core & Infrastructure
- [x] Core entities 구현 (User, Attendance, ChatActivity, ScoreConfig)
- [x] Database 모델 정의 (SQLAlchemy)
- [x] Alembic 마이그레이션 설정
- [x] 초기 마이그레이션 생성

### Phase 3: Business Logic
- [x] Repository 구현 (User, Attendance, ChatActivity, ScoreConfig)
- [x] Use cases 구현 (CheckIn, ProcessMessage, GetUserInfo, GetRanking)
- [x] Services 구현 (Attendance, ChatActivity, User)

### Phase 4: Handlers & Deployment (완성!)
- [x] `/시작` - 봇 시작 및 환영 메시지
- [x] `/도움말` - 상세 사용 가이드
- [x] `/출첵` - 출석 체크 및 신규 등록
- [x] 메시지 핸들러 - 채팅 보상 (잭팟 시스템)
- [x] `/내정보` - 개인 통계 및 기록 조회
- [x] `/랭킹` - 점수 순위 TOP 10
- [x] `/채팅랭킹` - 채팅 수 순위 TOP 10
- [x] `/잭팟랭킹` - 잭팟 횟수 순위 TOP 10
- [x] `/출석랭킹` - 연속 출석 순위 TOP 10
- [x] Docker 배포 설정 (Dockerfile, docker-compose.yml)
- [x] VPS 배포 스크립트 (deploy.sh)

## 📝 TODO

- [ ] 테스트 코드 작성
- [x] Docker 컨테이너화 ✅
- [ ] CI/CD 파이프라인 구축
- [x] VPS 배포 준비 완료 ✅

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Sasori** ([@voodoosim](https://github.com/voodoosim))

## 🙏 감사의 말

- [aiogram](https://github.com/aiogram/aiogram) - 훌륭한 비동기 Telegram Bot 프레임워크
- [SQLAlchemy](https://www.sqlalchemy.org/) - 강력한 Python ORM

---

**개발 시작일**: 2025-11-09
**상태**: 🔨 구현 중
