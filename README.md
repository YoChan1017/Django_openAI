# 🌏 SOLAIM

> **AI 기반 여행 추천 & 챗봇 백엔드 서비스**
>
> 퍼블릭 클라우드 DevSecOps 융합 인재 양성 과정 | Project_03

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-A30000?style=flat-square&logo=django&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat-square&logo=openai&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)

---

## 📌 프로젝트 소개

**SOLAIM**은 사용자가 입력한 여행지를 기준으로 관광지·식당·숙소 데이터를 조회하고, OpenAI API를 활용해 여행지에 대한 자연어 설명과 대화형 챗봇 응답을 제공하는 **Django REST Framework 기반 백엔드 서비스**입니다.

여행지 추천, 일정 생성, AI 챗봇 기능을 각각 Django App으로 분리하고, MySQL에 저장된 여행 데이터를 조회한 뒤 필요한 정보를 JSON 형태의 API 응답으로 제공합니다.

### 프로젝트 목표

- Django REST Framework 기반 REST API 설계 및 구현
- MySQL 기반 여행 데이터 조회 및 활용
- OpenAI API를 활용한 생성형 AI 기능 구현
- UUID 기반 챗봇 세션 및 대화 이력 관리
- Django Middleware를 활용한 만료 세션 정리
- 서버 측 임시 캐시를 활용한 추천 결과 상태 관리

---

## 🛠 기술 스택

| 구분 | 기술 |
|---|---|
| Language | Python 3 |
| Framework | Django 5.1.3 |
| API | Django REST Framework |
| AI | OpenAI API · GPT-4o-mini |
| Database | MySQL |
| DB Driver | mysqlclient · PyMySQL |
| Cache | In-memory Cache |
| Server | Gunicorn |
| Environment | python-dotenv |
| Test Dependency | pytest-django |

> Redis 및 `django-redis`는 의존성에 포함되어 있으나, 현재 주요 기능에서는 별도의 Redis 캐시 서버 대신 서버 메모리 기반 `CACHE` 딕셔너리를 사용합니다.

---

## ✨ 주요 기능

## 1. 🗺️ 여행지 관광지 추천

`POST /sol/travel/`

사용자가 입력한 여행지를 기준으로 관광지 데이터를 조회하고 최대 5개의 추천 결과를 반환합니다.

### 주요 기능

- 여행지 입력
- 관광지 데이터 지역 검색
- 관광지 5곳 랜덤 추천
- 추천 관광지 상세 조회
- OpenAI API를 이용한 관광지 설명 생성

### 처리 흐름

```text
여행지 입력
    ↓
Django REST API
    ↓
SQL Template
    ↓
MySQL 관광지 조회
    ↓
추천 결과 임시 저장
    ↓
JSON Response
```

관광지 데이터 조회에는 사전에 정의한 SQL Template과 파라미터 바인딩을 사용합니다.

---

## 2. 🗓️ 여행 일정 자동 생성

`POST /sol/calendar/`

여행지와 여행 기간을 기준으로 숙소·관광지·식당을 조합하여 일자별 여행 일정을 생성합니다.

### 일정 구성

하루 기준으로 다음 데이터를 조합합니다.

- 숙소 1곳
- 관광지 3곳
- 식당 2곳

### 주요 기능

- 여행지 및 여행 기간 입력
- 지역에 맞는 숙소 검색
- 숙소 주소에서 시·구·군 정보 추출
- 해당 지역의 관광지 검색
- 해당 지역의 식당 검색
- 일자별 랜덤 일정 구성
- 일정 항목별 상세 정보 조회
- OpenAI API를 이용한 장소 설명 생성

### 처리 흐름

```text
여행지 + 여행 기간
        ↓
숙소 조회
        ↓
주소에서 지역 정보 추출
        ↓
관광지 / 식당 조회
        ↓
랜덤 데이터 조합
        ↓
일자별 일정 생성
        ↓
JSON Response
```

---

## 3. 💬 AI 챗봇

### API

| Method | Endpoint | 설명 |
|---|---|---|
| POST | `/sol/chatbot/` | 챗봇 세션 생성 |
| POST | `/sol/chatbot/chat/` | 사용자 메시지 전송 |
| POST | `/sol/chatbot/log/` | 대화 이력 조회 |

### 주요 기능

- UUID 기반 세션 생성
- 여행지 및 여행 기간을 세션 정보로 저장
- 이전 대화 이력 조회
- 사용자 메시지에서 여행 관련 카테고리 판별
- 사전 정의 SQL Template을 이용한 DB 검색
- 검색 결과를 포함한 OpenAI API 응답 생성
- 사용자 메시지 및 AI 응답 저장
- 대화 이력 조회

### 처리 흐름

```text
사용자 메시지
      ↓
세션 확인
      ↓
키워드 기반 요청 유형 판별
      ↓
┌──────────────────────┐
│ 관광지 / 식당 / 숙소  │
└──────────┬───────────┘
           ↓
    SQL Template 선택
           ↓
        MySQL 조회
           ↓
      DB 검색 결과
           ↓
     OpenAI API 호출
           ↓
      자연어 응답 생성
           ↓
     대화 이력 저장
           ↓
      JSON Response
```

---

## 🏗️ 시스템 아키텍처

```text
┌──────────────────────────────┐
│           Client             │
│       Web / Mobile etc.      │
└──────────────┬───────────────┘
               │ HTTP
               ▼
┌──────────────────────────────┐
│        Django Router         │
└──────────────┬───────────────┘
               │
     ┌─────────┼─────────┐
     ▼         ▼         ▼
┌────────┐ ┌────────┐ ┌────────┐
│ Travel │ │ Chatbot│ │  Plan  │
└────┬───┘ └────┬───┘ └────┬───┘
     │           │          │
     └───────────┼──────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
┌───────────────┐  ┌────────────────┐
│    MySQL      │  │   OpenAI API   │
│               │  │   GPT-4o-mini  │
│ 여행 데이터    │  │ 자연어 생성     │
└───────────────┘  └────────────────┘
                 │
                 ▼
          JSON Response
```

---

## 📂 프로젝트 구조

```text
Django_openAI/
├── Django/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── sol/
│   ├── views.py
│   ├── models.py
│   ├── urls.py
│   └── sql_templates.py
│
├── travel/
│   ├── views.py
│   └── urls.py
│
├── chatbot/
│   ├── models.py
│   ├── views.py
│   ├── chatbot_chat.py
│   ├── middleware.py
│   └── urls.py
│
├── plan/
│   ├── views.py
│   └── urls.py
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🗄️ 데이터베이스

여행 서비스에 필요한 관광지·식당·숙소 데이터를 MySQL에서 관리하고, 챗봇의 세션 및 대화 이력은 Django Model을 통해 관리합니다.

### 여행 데이터

#### `attractions`

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

#### `restaurants`

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

#### `accommodations`

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

#### `ChatSession`

```text
ChatSession
├── session_id
├── location
├── days
└── created_at
```

#### `ChatMessage`

```text
ChatMessage
├── session
├── user_message
├── bot_response
└── timestamp
```

---

## 🔌 API 명세

### 관광지 추천

| Method | Endpoint | 설명 |
|---|---|---|
| POST | `/sol/travel/` | 여행지 관광지 추천 |
| GET | `/sol/travel/<id>/` | 추천 관광지 상세 정보 |

#### Request

```json
{
  "location": "서울"
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

| Method | Endpoint | 설명 |
|---|---|---|
| POST | `/sol/calendar/` | 여행 일정 생성 |
| GET | `/sol/calendar/<id>/` | 일정 항목 상세 정보 |

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
  "days": 3,
  "itinerary": [
    {
      "day": 1,
      "schedule": [
        {
          "id": 1,
          "name": "숙소 이름",
          "address": "서울 ...",
          "table": "accommodations"
        },
        {
          "id": 2,
          "name": "관광지 이름",
          "address": "서울 ...",
          "table": "attractions"
        },
        {
          "id": 3,
          "name": "식당 이름",
          "address": "서울 ...",
          "table": "restaurants"
        }
      ]
    }
  ]
}
```

---

### 챗봇 세션 생성

```json
{
  "location": "서울",
  "days": 3
}
```

#### Response

```json
{
  "session_id": "abc123...",
  "response": "안녕하세요! '서울'에서 3일 동안의 여행을 도와드릴게요."
}
```

### 챗봇 메시지

```json
{
  "session_id": "abc123...",
  "message": "서울에서 관광지 추천해줘"
}
```

#### Response

```json
{
  "session_id": "abc123...",
  "response": "..."
}
```

---

## 🔧 주요 구현

### 1. OpenAI API 연동

OpenAI API를 이용하여 관광지 및 일정 항목에 대한 자연어 설명과 챗봇 응답을 생성합니다.

```text
Django View
    ↓
Prompt 생성
    ↓
OpenAI API
    ↓
GPT-4o-mini
    ↓
자연어 응답
```

DB 검색 결과가 필요한 챗봇 요청은 먼저 데이터를 조회한 후 검색 결과를 프롬프트에 포함하여 AI 응답을 생성하도록 구성했습니다.

---

### 2. SQL Template + Parameter Binding

여행 데이터 검색에 필요한 SQL을 `sql_templates.py`에 사전 정의하고, 사용자 입력은 파라미터로 전달합니다.

```text
사용자 입력
    ↓
입력값 정리
    ↓
SQL Template 선택
    ↓
Parameter Binding
    ↓
MySQL Query
```

예를 들어 관광지 추천에는 지역 조건과 `ORDER BY RAND()`를 사용하여 최대 5개의 관광지를 조회합니다.

```sql
SELECT num, name, city, city2, city3, city4, bunnum, roadadd, x, y
FROM attractions
WHERE city LIKE %s
ORDER BY RAND()
LIMIT 5;
```

---

### 3. UUID 기반 챗봇 세션

챗봇 세션 생성 시 UUID를 발급하고, 해당 세션에 여행지·기간 정보를 저장합니다.

각 사용자의 메시지와 AI 응답은 `ChatMessage`로 연결하여 대화 이력을 관리합니다.

```text
ChatSession
     │
     ├── ChatMessage
     ├── ChatMessage
     └── ChatMessage
```

---

### 4. 만료 세션 정리 Middleware

세션 생성 후 10분이 지난 `ChatSession`을 대상으로 정리 작업을 수행하는 커스텀 Middleware를 구현했습니다.

```text
HTTP Request
     ↓
ExpiredSessionMiddleware
     ↓
10분 경과 세션 조회
     ↓
삭제
     ↓
실제 View 실행
```

정리 작업은 별도의 백그라운드 스케줄러가 아니라 **요청이 들어올 때 Middleware에서 수행**되도록 구현했습니다.

---

### 5. 추천 결과 임시 캐시

관광지 추천 결과를 서버 메모리의 `CACHE` 딕셔너리에 저장하여 상세 조회 시 기존 추천 결과를 다시 조회하지 않도록 구현했습니다.

```text
POST /sol/travel/
       ↓
DB 조회
       ↓
CACHE 저장
       ↓
GET /sol/travel/<id>/
       ↓
CACHE 조회
```

> 현재 캐시는 프로세스 메모리 기반의 임시 상태 저장 방식이므로, 다중 프로세스·다중 서버 환경에서는 공유되지 않는 한계가 있습니다.

---

## 🚨 기술적 고려사항

### SQL Injection 대응

SQL에 사용자 입력을 문자열로 직접 결합하지 않고 파라미터 바인딩 방식으로 전달하도록 구현했습니다.

### 입력값 검증

필수 파라미터 존재 여부와 `days` 값의 형식을 확인한 뒤 잘못된 요청에는 HTTP `400` 응답을 반환합니다.

### 예외 처리

DB 조회나 AI 응답 생성 과정에서 문제가 발생한 경우 오류 메시지와 적절한 HTTP 상태 코드를 반환하도록 처리했습니다.

### 환경 변수 관리

OpenAI API Key와 MySQL 접속 정보는 `python-dotenv`를 이용하여 환경 변수에서 읽도록 구성했습니다.

```env
OPENAI_API_KEY=your_openai_api_key

DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_NAME=your_db_name
DB_PORT=3306
```

---

## ⚙️ 실행 방법

### 1. 프로젝트 클론

```bash
git clone https://github.com/YoChan1017/Django_openAI.git
cd Django_openAI
```

### 2. 가상환경 생성 및 활성화

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

프로젝트 루트에 `.env` 파일을 생성하고 DB 및 OpenAI API 정보를 설정합니다.

### 5. 데이터베이스 마이그레이션

```bash
python manage.py migrate
```

### 6. 서버 실행

```bash
python manage.py runserver
```

---

## 📷 서비스 화면

### 여행지 추천

![SOLAIM 여행지 추천](https://github.com/user-attachments/assets/07b4744e-61bd-4e29-bfee-c6c2811b550c)

### 여행 일정 생성

![SOLAIM 여행 일정](https://github.com/user-attachments/assets/2c240dc5-a8e7-4889-a51e-970be531a45a)

### AI 챗봇

![SOLAIM AI 챗봇](https://github.com/user-attachments/assets/c147c6fc-1c64-469b-9d68-0fc4f188a669)

---

## 📚 프로젝트를 통해 경험한 내용

- Django REST Framework 기반 API 개발
- MySQL 데이터베이스 연동 및 SQL 작성
- Parameter Binding 기반 DB 조회
- OpenAI API 연동 및 프롬프트 구성
- UUID 기반 세션 관리
- Django Middleware 작성
- 서버 메모리 기반 임시 상태 관리
- 외부 클라이언트와 JSON 기반 데이터 통신
- Gunicorn 기반 WSGI 서버 구성
- Python 가상환경 및 환경 변수 관리

---

## 🔮 개선 방향

### 캐시 구조 개선

현재 서버 메모리 기반 `CACHE`를 Redis와 같은 외부 저장소로 변경하여 다중 프로세스 및 다중 서버 환경에서도 공유 가능한 캐시 구조로 개선할 수 있습니다.

### API 구조 개선

- 요청/응답 Schema 검증 강화
- 공통 예외 처리 구조 도입
- API 인증 및 사용자별 데이터 관리
- OpenAPI 기반 API 문서화

### 데이터 처리 개선

- 대규모 데이터 조회를 고려한 인덱스 설계
- `ORDER BY RAND()` 사용 방식 개선
- DB 연결 관리 및 쿼리 구조 개선

### AI 기능 개선

- OpenAI API 호출 비용 최적화
- 응답 시간 개선
- 프롬프트 구조 개선
- 생성 결과의 안정적인 형식 관리

---

## 🔗 Repository

https://github.com/YoChan1017/Django_openAI
