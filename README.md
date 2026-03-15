# 🌏 SOLAIM — AI 기반 여행 추천 & 챗봇 백엔드

> **퍼블릭 클라우드 DevSecOps 융합 인재 양성 과정 | Project_03**  
> Python · Django · OpenAI API · MySQL · Redis · REST Architecture

---

## 📌 프로젝트 개요

**SOLAIM**은 사용자가 입력한 여행지(location)와 여행 기간(days)을 기반으로 관광지·식당·숙소 데이터를 분석하고, OpenAI GPT를 활용해 자연어 설명과 대화형 챗봇 서비스를 제공하는 **AI 여행 추천 백엔드 시스템**입니다.

Django REST Framework 기반 API 서버로 설계되어, 외부 프론트엔드 또는 모바일 앱과 독립적으로 통신할 수 있습니다.

---

## 🎯 개발 목적

- OpenAI API를 활용한 **생성형 AI 서비스 백엔드 구현** 경험
- Django REST Framework 기반 **RESTful API 서버 설계** 역량 습득
- 세션 관리·미들웨어·DB 연동 등 **Django 심화 기능** 실습
- MySQL 기반 데이터 파이프라인과 **SQL 템플릿 패턴** 적용

---

## 🛠 기술 스택

| 분류 | 기술 |
|------|------|
| 언어 | Python 3 |
| 웹 프레임워크 | Django 5.1 · Django REST Framework |
| AI / 자연어 처리 | OpenAI API (GPT-4o-mini) |
| 데이터베이스 | MySQL (mysqlclient · pymysql) |
| 캐시 | Redis (django-redis) |
| 서버 | Gunicorn |
| 환경 관리 | python-dotenv |
| 테스트 | pytest-django |

---

## 📁 프로젝트 구조

```
Django_openAI/
├── Django/          # 프로젝트 설정 (settings.py, urls.py)
├── sol/             # OpenAI 호출 및 SQL 템플릿 관리
├── travel/          # 여행지 기반 관광지 추천
├── chatbot/         # 세션 기반 챗봇 로직
├── plan/            # 여행 일정 생성
├── manage.py
├── requirements.txt
└── .env             # OpenAI Key / DB 접속 정보
```

---

## ✨ 주요 기능

### 1. 여행지 관광지 추천 (`/sol/travel/`)

- `POST` 요청으로 여행지와 일수를 입력하면 DB에서 관광지 5곳을 랜덤 추천
- `GET /<id>/` 로 특정 관광지 선택 시 OpenAI가 자연어 설명을 실시간 생성

### 2. 여행 일정 자동 생성 (`/sol/calendar/`)

- 여행지·기간을 입력하면 **일자별 숙소 1곳 · 관광지 3곳 · 식당 2곳**으로 구성된 스케줄 자동 배정
- 주소에서 시/구 단위를 파싱하여 지역 데이터 정밀 필터링
- `GET /<days>/<id>/` 로 특정 일정 항목 조회 시 GPT 설명 생성

### 3. AI 챗봇 (`/sol/chatbot/`)

- 세션 기반 대화 관리 (UUID 세션 ID 발급)
- 사용자 메시지 키워드 분석 후 DB 검색 + GPT 응답 통합 생성
- 대화 이력 누적 및 `/log` 엔드포인트로 조회 가능
- **미들웨어**를 통해 10분 경과 세션 자동 삭제 (성능 최적화)

---

## 🗄 데이터베이스 구조

```sql
-- 관광지
attractions (num, name, city, city2, city3, city4, bunnum, roadadd, x, y)

-- 식당
restaurants (num, call, post, address, name, x, y)

-- 숙소
accommodations (num, name, address, latitude, longitude, cat)

-- 챗봇 세션 (Django 모델)
chatbot_chatsession   -- 세션 ID, 여행지, 기간, 생성시각
chatbot_chatmessage   -- 세션 FK, 사용자 메시지, 봇 응답, 타임스탬프
```

---

## 🔌 API 명세

### 관광지 추천

| Method | Endpoint | 설명 |
|--------|----------|------|
| `POST` | `/sol/travel/` | 여행지 관광지 5곳 추천 |
| `GET` | `/sol/travel/<id>/` | 특정 관광지 상세 정보 + AI 설명 |

**요청 예시**
```json
{ "location": "서울", "days": 3 }
```

**응답 예시**
```json
{
  "location": "서울",
  "recommendations": [
    { "id": 1, "name": "경복궁", "address": "서울 종로구 ...", "latitude": "37.57", "longitude": "126.97" }
  ]
}
```

---

### 여행 일정 생성

| Method | Endpoint | 설명 |
|--------|----------|------|
| `POST` | `/sol/calendar/` | 전체 여행 일정 생성 |
| `GET` | `/sol/calendar/<id>/` | 특정 일정 항목 상세 조회 |

**응답 예시**
```json
{
  "itinerary": [
    {
      "day": 1,
      "schedule": [
        { "id": 1, "name": "그랜드하얏트", "table": "accommodations", "address": "..." },
        { "id": 2, "name": "남산타워", "table": "attractions", "address": "..." }
      ]
    }
  ]
}
```

---

### 챗봇

| Method | Endpoint | 설명 |
|--------|----------|------|
| `POST` | `/sol/chatbot/` | 챗봇 세션 생성 |
| `POST` | `/sol/chatbot/chat/` | 대화 메시지 전송 |
| `POST` | `/sol/chatbot/log/` | 대화 이력 조회 |

**세션 생성 응답 예시**
```json
{
  "session_id": "abc123...",
  "response": "안녕하세요! '서울'에서 3일 동안의 여행을 도와드릴게요."
}
```

---

## ⚙️ 실행 방법

```bash
# 1. 가상환경 생성 및 활성화
python -m venv vm
source vm/bin/activate          # Windows: vm\Scripts\activate

# 2. 패키지 설치
pip install -r requirements.txt

# 3. 환경 변수 설정 (.env)
# OPENAI_API_KEY, DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT

# 4. 마이그레이션 및 서버 실행
python manage.py makemigrations chatbot
python manage.py migrate
python manage.py runserver
```

---

## 🏗 아키텍처 설명

```
클라이언트 요청
    ↓
Django URL Router (Django/urls.py)
    ↓
각 앱 View (travel / chatbot / plan)
    ↓
sol/views.py → OpenAI API 호출 (GPT-4o-mini)
    ↓         → SQL Templates 실행 (sol/sql_templates.py)
    ↓
MySQL DB (관광지 / 식당 / 숙소 데이터)
    ↓
JSON 응답 반환
```

**주요 설계 결정:**
- SQL 인젝션 방지를 위해 Raw SQL 대신 **파라미터 바인딩 + 사전 정의 템플릿** 사용
- 챗봇 세션 만료를 **Request 훅 미들웨어**에서 비동기적으로 처리 (10분 주기 일괄 삭제)
- 관광지 추천 결과를 서버 메모리 `CACHE` 딕셔너리에 임시 보관하여 상세 조회 시 DB 재조회 최소화

---

## 🔒 보안 고려사항

- API 키 및 DB 접속 정보는 `.env` 파일로 분리, 코드에 하드코딩하지 않음
- 미들웨어를 통한 만료 세션 자동 삭제로 불필요한 사용자 데이터 최소화
- CSRF 데코레이터 적용 및 Django 기본 보안 미들웨어 활성화

---

## 📄 라이선스

본 프로젝트는 교육 목적의 포트폴리오 프로젝트입니다.
