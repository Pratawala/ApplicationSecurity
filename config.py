from os import environ, path
from dotenv import load_dotenv
import ast

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))
SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_BINDS = ast.literal_eval(environ.get("SQLALCHEMY_BINDS"))
SESSION_PERMANENT = False
SESSION_COOKIE_SECURE = True
SECRET_KEY = environ.get("SECRET_KEY")
MAIL_SERVER='smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = 'larosefaneeapp@gmail.com'
MAIL_PASSWORD = environ.get("MAIL_PASSWORD")
MAIL_USE_TLS = False
MAIL_USE_SSL = True