# 퍼블릭 클라우드 DevSecOps 융합 인재 양성 과정 
> Project_03_SOLAIM

## Project Overview
> SOLAIM_Django_openAI<br>
> Python · Django · OpenAI API · REST Architecture








<br><br><br><br><br>

프로젝트 실행 방법
<br><br>
.env 파일 설정<br>
OPENAI_API_KEY 작성<br>
MySQL 계정 작성<br>
<br>
프로젝트 내 vm 폴더 ( 가상환경 ) 삭제 후 재설치
> python -m venv vm

프로젝트 세팅
> vm/Scripts/activate<br>
> pip install -r requirements.txt<br>
> python manage.py makemigrations chatbot<br>
> python manage.py migrate<br>

프로젝트 실행
> python manage.py runserver
<br>
<br>
테스트 방법<br>
- Postman - API 명세표 참고<br>
<br>
- 챗봇 : 좀 더 자연스러운 대화 및 sql 템플릿 필요<br>
- 적은 데이터로 인해 AI설명 불일치<br>
<br><br>
데이터셋<br>
accommodations			숙소 데이터<br>
attractions			관광 데이터<br>
restaurants			식당 데이터<br>
<br>
챗봇 관리용 (시간 지나면 자동 삭제)<br>
chatbot_chatmessage		챗봇_세션에 따른 메세지기록<br>
chatbot_chatsession		챗봇_사용자 세션 기록<br>
<br>
Django 자동 생성 테이블<br>
auth_group			사용자 그룹 관리<br>
auth_group_permissions		그룹과 권한 간의 관계를 관리<br>
auth_permission			Django의 권한 시스템에서 사용되는 권한 정의<br>
auth_user			Django의 기본 사용자 모델<br>
auth_user_groups			사용자와 그룹 간의 관계를 관리<br>
auth_user_user_permissions		사용자와 권한 간의 관계를 관리<br>
django_admin_log			Django 관리자 페이지에서 수행된 작업 로그를 저장<br>
django_content_type		Django에서 사용되는 모든 모델의 정보를 저장<br>
django_migrations			Django의 마이그레이션 기록<br>
django_session			사용자 세션 데이터를 저장<br>
