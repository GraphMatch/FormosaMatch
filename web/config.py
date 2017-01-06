# config.py


import os


class BaseConfig(object):
    SECRET_KEY = os.environ['SECRET_KEY']
    DEBUG = os.environ['DEBUG']
    DB_NAME = os.environ['DB_NAME']
    DB_USER = os.environ['DB_USER']
    DB_PASS = os.environ['DB_PASS']
    DB_SERVICE = os.environ['DB_SERVICE']
    DB_PORT = os.environ['DB_PORT']
    SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
        DB_USER, DB_PASS, DB_SERVICE, DB_PORT, DB_NAME
    )
    SECURITY_PASSWORD_SALT = '5(15ds+i2+%ik6z&!yer+ga9m=e%jcqiz_5wszg)r-z!2--b2d'

    # mail settings (gmail)
    MAIL_SERVER = os.environ['MAIL_SERVER']
    MAIL_PORT = os.environ['MAIL_PORT']
    MAIL_USE_TLS = os.environ['MAIL_USE_TLS']
    MAIL_USE_SSL = os.environ['MAIL_USE_SSL']

    # gmail authentication
    MAIL_USERNAME = os.environ['MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['MAIL_PASSWORD']

    # mail accounts
    MAIL_DEFAULT_SENDER = os.environ['MAIL_DEFAULT_SENDER']
    UPLOAD_FOLDER = os.environ['UPLOAD_FOLDER']

# If leaving hard-coded:
# class BaseConfig(object):
#     SECRET_KEY = 'hi'
#     DEBUG = True
#     DB_NAME = 'postgres'
#     DB_SERVICE = 'localhost'
#     DB_PORT = 5432
#     SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}/{2}'.format(
#         DB_SERVICE, DB_PORT, DB_NAME
#     )
