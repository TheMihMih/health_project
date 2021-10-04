from flask_sqlalchemy import SQLAlchemy
<<<<<<< HEAD
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f"<User name - {self.username}, User ID = {self.id}>"
=======

db = SQLAlchemy()

class BDConnector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, unique=True, nullable=False)
    text = db.Column(db.Text, nullable=True)
    category = db.Column(db.Integer, nullable=True) #Какие категории? Спорт, питание... Возможно стоит сделать не Int, а String
    published = db.Column(db.DateTime, nullable=False)
    
    def __repr__(self):
        return '<News {} {}>'.format(self.title, self.url)

>>>>>>> aafe73ee198626047798ed04836a4120b329e4f8
