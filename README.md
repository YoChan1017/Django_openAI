Django API Server Backup
<br><br>
* vm 폴더 ( 가상환경 ) 삭제 후 재설치 <br>
> python -m venv vm
<br><br>
1. > vm/Scripts/activate
<br>
2. > pip install -r requirements.txt
<br>
3. > python manage.py makemigrations chatbot
<br>
3. > python manage.py migrate
<br>
4. > python manage.py runserver
<br>
