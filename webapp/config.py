import os

basedir = os.path.abspath(os.path.dirname(__file__))


SECRET_KEY = '[B\xcb\r\xa18\x87[+\x8a\x9fIm1\x9dZ'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')