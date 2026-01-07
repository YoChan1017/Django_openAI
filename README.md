# 퍼블릭 클라우드 DevSecOps 융합 인재 양성 과정 
Project_03_SOLAIM <br>
OpenAI 기반 여행 일정 추천 및 챗봇 백엔드 서비스

> SOLAIM - Django_openAI<br>
> Python · Django · OpenAI API · REST Architecture · MySQL


## 프로젝트 개요

**Django_openAI**는 **SOLAIM** 프로젝트에서 OpenAI 연동, 여행 데이터 처리, 일정 생성 및 세션 기반 챗봇 로직을 전담하는 백엔드 API 서버로 만들어졌습니다.

Django_openAI(SOLAIM)는 사용자가 입력한 여행지(location)와 여행 기간(days)을 기반으로 관광지·식당·숙소 데이터를 분석하고 **OpenAI API**를 활용해 자연어 설명과 대화형 챗봇 서비스를 제공하는 AI 여행 추천 백엔드 시스템입니다.


## 개발 목적

- OpenAI API를 활용한 **생성형 AI 서비스 백엔드 구현**

- Django REST Framework 기반 **API 서버 설계 경험**


## 기술 스택

- Python 
- Django 
- Django REST Framework
- Gunicorn
- OpenAI API (GPT)
- MySQL 
- Redis


## 주요 파일 및 기능

Django_openAI/                                

├─ Django/              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# 프로젝트 설정 (settings, urls) 

├─ sol/                 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# OpenAI 호출 및 SQL 템플릿 관리  

├─ travel/              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# 여행지 기반 관광지 추천         

├─ chatbot/             &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# 세션 기반 챗봇 로직       

├─ plan/                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# 여행 일정 생성                 

├─ manage.py                                            

├─ requirements.txt                                   

├─ .env                 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# OpenAI Key / DB 정보         

└─ vm/                  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Python 가상환경           
