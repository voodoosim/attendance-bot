# 📝 Attendance Bot

> Telegram 출석 봇 - Clean Architecture를 적용한 현대적인 출석 관리 시스템

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![aiogram](https://img.shields.io/badge/aiogram-3.13.1-blue.svg)](https://github.com/aiogram/aiogram)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🎯 주요 기능

### 사용자 기능
- ✅ **출석 체크**: `/출석` 또는 `/check_in` 명령어로 간편 출석
- ✅ **출석 현황**: 개인 출석 기록 및 통계 조회
- ✅ **연속 출석**: 연속 출석일 자동 계산 및 표시
- ✅ **출석 리마인더**: 설정한 시간에 자동 알림
- ✅ **그룹 랭킹**: 그룹 내 출석 순위 확인

### 관리자 기능
- ✅ **출석 관리**: 출석 데이터 조회 및 수정
- ✅ **통계 조회**: 일/주/월별 출석 통계
- ✅ **사용자 관리**: 사용자 목록 및 상태 관리
- ✅ **시스템 설정**: 봇 설정 및 관리

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

### 4. 실행

```bash
# 봇 실행
python main.py
```

## 📋 명령어 목록

### 사용자 명령어
| 명령어 | 설명 |
|--------|------|
| `/start` | 봇 시작 및 안내 메시지 |
| `/출석` 또는 `/check_in` | 출석 체크 |
| `/내출석` 또는 `/my_attendance` | 내 출석 현황 조회 |
| `/통계` 또는 `/stats` | 출석 통계 보기 |
| `/랭킹` 또는 `/ranking` | 그룹 출석 순위 |
| `/알림설정` 또는 `/set_reminder` | 출석 알림 설정 |

### 관리자 명령어
| 명령어 | 설명 |
|--------|------|
| `/admin` | 관리자 메뉴 |
| `/reset` | 출석 데이터 초기화 |
| `/users` | 사용자 목록 조회 |
| `/export` | 출석 데이터 내보내기 |

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

## 📝 TODO

- [ ] Core entities 구현
- [ ] Use cases 구현
- [ ] Repository 구현
- [ ] Handler 구현
- [ ] Database 모델 정의
- [ ] Alembic 마이그레이션 설정
- [ ] 테스트 코드 작성
- [ ] Docker 컨테이너화
- [ ] CI/CD 파이프라인 구축

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
