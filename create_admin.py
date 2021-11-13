import sys

from getpass import getpass
from webapp import create_app
from webapp.db import db
from webapp.user.models import User

app = create_app()

with app.app_context():
    username = input("Введите имя: ")

    if User.query.filter(User.username == username).count():
        print("Пользователь с таким именем уже существует!!!")
        sys.exit(0)

    email = input("Email: ")

    if User.query.filter(User.email == email).count():
        print("Пользователь с такой почтой уже существует!!!")
        sys.exit(0)

    password1 = getpass("Введите пароль:")
    password2 = getpass("Повторите пароль:")

    if password1 != password2:
        print("Пароль не одинаковый!")
        sys.exit(0)

    admin = User(username=username, email=email, role="admin")
    admin.set_password(password1)

    db.session.add(admin)
    db.session.commit()

    print(f"Создан пользователь с id={admin.id}")
