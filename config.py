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
