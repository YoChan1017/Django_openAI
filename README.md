Django API Server Backup
<br><br>
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
