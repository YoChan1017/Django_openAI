# 🌏 SOLAIM — AI 기반 여행 추천 & 챗봇 백엔드

> **퍼블릭 클라우드 DevSecOps 융합 인재 양성 과정 | Project_03**  
> Python · Django · Django REST Framework · OpenAI API · MySQL · Redis

## 📌 프로젝트 소개

**SOLAIM**은 사용자가 입력한 여행지와 여행 기간을 기반으로 관광지·식당·숙소 데이터를 조회하고, OpenAI GPT를 활용해 여행 정보에 대한 자연어 설명과 대화형 챗봇을 제공하는 **AI 여행 추천 백엔드 서비스**입니다.

Django REST Framework를 기반으로 REST API 서버를 구성하여, 웹 프론트엔드나 모바일 애플리케이션과 독립적으로 통신할 수 있도록 설계했습니다.

### 프로젝트 목표

- 생성형 AI API를 백엔드 서비스에 연동
- Django REST Framework 기반 REST API 설계 및 구현
- MySQL을 활용한 여행 데이터 관리
- 세션 기반 챗봇과 대화 이력 관리
- Redis 및 서버 측 캐시를 활용한 데이터 처리 구조 경험
- 미들웨어를 활용한 세션 관리 및 데이터 정리

---

## 🛠 기술 스택

| 구분 | 기술 |
|---|---|
| Language | Python 3 |
| Framework | Django 5.1 |
| API | Django REST Framework |
| AI | OpenAI API, GPT-4o-mini |
| Database | MySQL |
| Cache | Redis, django-redis |
| Server | Gunicorn |
| Environment | python-dotenv |
| Test | pytest-django |

---

## ✨ 주요 기능

### 1. 여행지 관광지 추천

`/sol/travel/`

사용자가 여행지와 여행 기간을 입력하면 해당 지역의 관광지 데이터를 조회하여 추천 목록을 제공합니다.

- 여행지 및 여행 기간 입력
- 관광지 5곳 추천
- 관광지 상세 정보 조회
- OpenAI API를 이용한 관광지 자연어 설명 생성

### 2. 여행 일정 자동 생성

`/sol/calendar/`

여행지와 기간을 기준으로 숙소·관광지·식당 데이터를 조합하여 일자별 여행 일정을 생성합니다.

- 일자별 여행 일정 생성
- 숙소 1곳
- 관광지 3곳
- 식당 2곳
- 주소에서 지역 정보를 추출하여 데이터 필터링
- 일정 항목 상세 조회
- OpenAI API를 이용한 일정 정보 설명 생성

### 3. AI 챗봇

`/sol/chatbot/`

여행지와 여행 기간을 기반으로 사용자와 대화할 수 있는 세션 기반 AI 챗봇을 제공합니다.

- UUID 기반 세션 생성
- 사용자 메시지 분석
- 데이터베이스 검색 결과와 GPT 응답 결합
- 대화 이력 저장 및 조회
- 세션 만료 데이터 자동 정리

---

## 🏗 시스템 아키텍처

```text
┌──────────────────────┐
│      Client          │
│ Web / Mobile / etc. │
└──────────┬───────────┘
           │ HTTP Request
           ▼
┌──────────────────────┐
│   Django URL Router  │
└──────────┬───────────┘
           ▼
┌─────────────────────────────────┐
│          Django Apps            │
│                                 │
│ travel │ chatbot │ plan │ sol   │
└──────────────┬──────────────────┘
               │
       ┌───────┴────────┐
       ▼                ▼
┌──────────────┐  ┌────────────────┐
│   MySQL      │  │  OpenAI API    │
│              │  │   GPT-4o-mini  │
│ 여행 데이터   │  │ AI 응답 생성   │
└──────────────┘  └────────────────┘
               │
               ▼
        ┌──────────────┐
        │ JSON Response│
        └──────────────┘
```

### Django Application 구조

```text
Django_openAI/
├── Django/
│   ├── settings.py
│   └── urls.py
│
├── sol/
│   ├── views.py
│   └── sql_templates.py
│
├── travel/
│   └── views.py
│
├── chatbot/
│   ├── models.py
│   └── views.py
│
├── plan/
│   └── views.py
│
├── manage.py
└── requirements.txt
```

---

## 🗄 데이터베이스

### 여행 데이터

```text
attractions
├── num
├── name
├── city
├── city2
├── city3
├── city4
├── bunnum
├── roadadd
├── x
└── y
```

```text
restaurants
├── num
├── call
├── post
├── address
├── name
├── x
└── y
```

```text
accommodations
├── num
├── name
├── address
├── latitude
├── longitude
└── cat
```

### 챗봇 데이터

Django Model을 활용하여 세션과 대화 이력을 관리합니다.

```text
chatbot_chatsession
├── session_id
├── location
├── days
└── created_at

chatbot_chatmessage
├── session
├── user_message
├── bot_response
└── timestamp
```

---

## 🔌 API

### 관광지 추천

| Method | Endpoint | Description |
|---|---|---|
| POST | `/sol/travel/` | 여행지 관광지 5곳 추천 |
| GET | `/sol/travel/<id>/` | 관광지 상세 정보 및 AI 설명 |

#### Request

```json
{
  "location": "서울",
  "days": 3
}
```

#### Response

```json
{
  "location": "서울",
  "recommendations": [
    {
      "id": 1,
      "name": "경복궁",
      "address": "서울 종로구 ...",
      "latitude": "37.57",
      "longitude": "126.97"
    }
  ]
}
```

---

### 여행 일정 생성

| Method | Endpoint | Description |
|---|---|---|
| POST | `/sol/calendar/` | 전체 여행 일정 생성 |
| GET | `/sol/calendar/<id>/` | 일정 항목 상세 조회 |

#### Response

```json
{
  "itinerary": [
    {
      "day": 1,
      "schedule": [
        {
          "id": 1,
          "name": "그랜드하얏트",
          "table": "accommodations",
          "address": "..."
        },
        {
          "id": 2,
          "name": "남산타워",
          "table": "attractions",
          "address": "..."
        }
      ]
    }
  ]
}
```

---

### AI 챗봇

| Method | Endpoint | Description |
|---|---|---|
| POST | `/sol/chatbot/` | 챗봇 세션 생성 |
| POST | `/sol/chatbot/chat/` | 사용자 메시지 전송 |
| POST | `/sol/chatbot/log/` | 대화 이력 조회 |

#### Session Response

```json
{
  "session_id": "abc123...",
  "response": "안녕하세요! '서울'에서 3일 동안의 여행을 도와드릴게요."
}
```

---

## 🔧 주요 구현

### 1. OpenAI API 연동

여행지 및 관광지에 대한 설명을 생성하기 위해 OpenAI API를 백엔드에서 호출하도록 구현했습니다.

```text
Client
  ↓
Django View
  ↓
OpenAI API
  ↓
Generated Response
  ↓
JSON Response
```

이를 통해 정적인 관광지 데이터뿐 아니라 사용자의 요청에 따라 생성되는 자연어 정보를 함께 제공하도록 구성했습니다.

### 2. SQL Template 기반 데이터 조회

여행지 검색에 필요한 SQL을 사전에 정의하고, 사용자 입력값은 파라미터 바인딩 방식으로 전달하도록 구성했습니다.

```text
User Input
    ↓
Location / Days Validation
    ↓
Predefined SQL Template
    ↓
Parameterized Query
    ↓
MySQL
```

이를 통해 사용자 입력을 SQL 문자열에 직접 결합하지 않고 데이터 조회를 수행하도록 구현했습니다.

### 3. 세션 기반 챗봇

챗봇은 UUID 기반 세션을 생성하고 해당 세션에 사용자 메시지와 GPT 응답을 연결하여 대화 이력을 관리합니다.

```text
Chat Session
     │
     ├── User Message
     ├── Bot Response
     ├── User Message
     └── Bot Response
```

세션이 일정 시간 이상 유지되지 않도록 만료 데이터를 자동으로 정리하는 미들웨어도 구현했습니다.

### 4. 추천 결과 임시 캐시

관광지 추천 결과는 서버 메모리의 `CACHE` 딕셔너리에 임시 보관하여 상세 조회 과정에서 불필요한 재조회가 발생하지 않도록 구성했습니다.

---

## 🚨 기술적 고려사항

### SQL Injection 방지

사용자 입력을 SQL 문자열에 직접 연결하는 방식 대신, 사전에 정의한 SQL Template과 파라미터 바인딩을 사용하도록 구성했습니다.

### 세션 데이터 관리

챗봇 세션은 일정 시간이 지나면 만료되도록 구성하고, 미들웨어를 통해 오래된 세션 데이터를 자동으로 정리합니다.

### 환경 변수 분리

OpenAI API Key 및 데이터베이스 접속 정보를 코드와 분리하여 환경 변수로 관리하도록 구성했습니다.

```text
OPENAI_API_KEY
DB_USER
DB_PASSWORD
DB_HOST
DB_NAME
DB_PORT
```

---

## ⚙️ 실행 방법

### 1. 프로젝트 클론

```bash
git clone https://github.com/YoChan1017/Django_openAI.git
cd Django_openAI
```

### 2. 가상환경 생성

```bash
python -m venv vm
```

#### Windows

```bash
vm\Scripts\activate
```

#### macOS / Linux

```bash
source vm/bin/activate
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정

프로젝트 루트에 `.env` 파일을 생성하고 다음 항목을 설정합니다.

```env
OPENAI_API_KEY=your_openai_api_key

DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_NAME=your_db_name
DB_PORT=your_db_port
```

### 5. 데이터베이스 마이그레이션

```bash
python manage.py makemigrations chatbot
python manage.py migrate
```

### 6. 개발 서버 실행

```bash
python manage.py runserver
```

---

## 📷 서비스 실행 화면

### 여행지 추천

<img width="1656" height="800" alt="SOLAIM 여행지 추천" src="https://github.com/user-attachments/assets/07b4744e-61bd-4e29-bfee-c6c2811b550c" />

### 여행 일정 생성

<img width="1656" height="800" alt="SOLAIM 여행 일정" src="https://github.com/user-attachments/assets/2c240dc5-a8e7-4889-a51e-970be531a45a" />

### AI 챗봇

<img width="1645" height="800" alt="SOLAIM AI 챗봇" src="https://github.com/user-attachments/assets/c147c6fc-1c64-469b-9d68-0fc4f188a669" />

---

## 📚 프로젝트를 통해 경험한 내용

- Django REST Framework 기반 API 서버 설계
- 외부 AI API를 활용한 생성형 AI 서비스 구현
- MySQL 기반 데이터 조회 및 관리
- SQL Template 및 Parameter Binding을 활용한 데이터 접근
- UUID 기반 세션 관리
- Django Middleware를 이용한 세션 데이터 관리
- Redis 및 서버 측 캐시 활용
- Gunicorn 기반 서버 실행 환경 구성
- REST API와 외부 클라이언트 간 데이터 통신 구조 설계

---

## 🔮 개선 방향

현재 구조를 기반으로 다음과 같은 개선을 고려할 수 있습니다.

- 추천 결과 캐시를 Redis 기반으로 통합하여 서버 확장성 개선
- API 예외 처리 및 입력값 검증 강화
- 테스트 코드 확대
- API 인증 및 사용자별 서비스 상태 관리
- Docker 기반 배포 환경 구성
- API 문서 자동화 및 관리
- OpenAI API 호출 비용 및 응답 시간 최적화

---

## 🔗 Repository

[GitHub - YoChan1017/Django_openAI](https://github.com/YoChan1017/Django_openAI)
