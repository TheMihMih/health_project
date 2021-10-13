from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import RoleMixin

db = SQLAlchemy()

roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id")),
)


class Role(db.Model, RoleMixin):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f"<Role - {self.name}>"


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

    @property
    def is_admin(self):
        return self.role == "admin"

    def __repr__(self):
        return f"<User name - {self.username}, User ID = {self.id}>"


class BDConnector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.Text, nullable=True)
<<<<<<< HEAD
    category = db.Column(
        db.Integer, nullable=True
    )  # Какие категории? Спорт, питание... Возможно стоит сделать не Int, а String
    published = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<News {self.title} {self.url}>"
=======
    category = db.Column(db.String, nullable=True) #Какие категории? Спорт, питание... Возможно стоит сделать не Int, а String

    
    def __repr__(self):
        return f'<News {self.title} {self.category}>'
>>>>>>> b527cc67422bd78f321ba4e43de9f2ec3d51f904
