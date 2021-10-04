import os

basedir = os.path.abspath(os.path.dirname(__file__))

<<<<<<< HEAD
SECRET_KEY = '[B\xcb\r\xa18\x87[+\x8a\x9fIm1\x9dZ'
=======

>>>>>>> aafe73ee198626047798ed04836a4120b329e4f8
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')