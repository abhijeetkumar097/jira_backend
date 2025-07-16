import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'AJAOFEEOIF0290KJSAFAFJAOFEJAWFOIAFEIFIEWIAA'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=50)
    SECRET_KEY = 'mysecretkey'
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME='xyz@gmail.com'
    MAIL_PASSWORD='xxxx xxxx xxxx xxxx'