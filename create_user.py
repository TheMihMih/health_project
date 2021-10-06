from flask.helpers import flash
from webapp.model import db, User

def create_and_add_user(username, email, password):
    user = User.query.filter(User.username == username).count()
    flash(f"Пользователь с именем {username} уже существует!!!")
    if not user:
        new_user = User(username=username, email=email, password=password, role='user')
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()