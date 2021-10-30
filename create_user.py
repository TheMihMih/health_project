from flask.helpers import flash
from webapp.db import db
from webapp.user.models import User

def create_and_add_user(username, email, password):
    user_name = User.query.filter(User.username == username).count()
    user_email = User.query.filter(User.email == email).count()
    if user_name:
        flash(f"Пользователь с именем {username} уже существует!!!")
    elif user_email:
        flash(f"Пользователь с почтой {email} уже существует!!!")
    else:
        flash(f"Создан пользователь {username}")
        new_user = User(username=username, email=email, password=password, role='user')
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        