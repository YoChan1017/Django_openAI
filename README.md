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
앞으로 해결해야 할 일<br>
- 챗봇 : 좀 더 자연스러운 대화 및 sql 템플릿 필요<br>
- 적은 데이터로 인해 AI설명 불일치<br>
