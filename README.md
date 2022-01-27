# Проект HealthProject 

HealthProject помогает Вам следить за тем, что Вы едите!

## Установка 

1. Клонируйте репозиторий 
2. Создайте виртуальное окружение
3. Установите зависимости `pip install -r requirements.txt`
4. Создайте  файл `config.py`
5. Впишите в config.py переменные:
```
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')

SECRET_KEY = Ваш ключ
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

SQLALCHEMY_TRACK_MODIFICATIONS = False
```
6. Запустите celery и командой `celery -A tasks worker --loglevel=info` для Linux/Mac
   или `set FORKED_BY_MULTIPROCESSING=1 && celery -A tasks worker --loglevel=info` для Win

7. Запустите проект с помощью файла `run.sh` для Linux/Mac или `run.bat` для Win