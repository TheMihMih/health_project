from webapp.model import db, User

def create_and_add_user(username, email, password):
    user = User(username=username, email=email, password=password, role='user')
    user.set_password(password)

    db.session.add(user)
    db.session.commit()