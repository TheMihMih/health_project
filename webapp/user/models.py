from webapp.db import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True, default="user")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == "admin"

    def __repr__(self):
        return f"<User name - {self.username}, User ID = {self.id}>"


class PersonalData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_weight = db.Column(db.Integer)
    user_height = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    purpouse = db.Column(db.String(50))
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),
        index=True
    )
    user = relationship('User', backref='Personal_Data')