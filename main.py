from flask import Flask
from flask import request
from datetime import timedelta
from flask import session as user_session
from flask_sqlalchemy import SQLAlchemy
from tools.random_key import get_random_string
from flask_login import LoginManager
from urllib.parse import urlparse, urljoin
from flask_bcrypt import Bcrypt

login_manager = LoginManager()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.sqlite3'
app.config['SQLALCHEMY_BINDS'] = {'product' : 'sqlite:///product.sqlite3'}
app.config['SECRET_KEY'] = "randP@55string"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_COOKIE_SECURE"] = True
db = SQLAlchemy(app)
login_manager.init_app(app)
bcrypt = Bcrypt(app)

class Users_db(db.Model):
  
  username = db.Column("username",db.String, primary_key=True)
  password = db.Column(db.String(100))
  token = db.Column(db.String(100))
  admin = db.Column(db.Boolean)
  cart = db.Column(db.String(1000))
  login_attempt = db.Column(db.Integer)
  active = db.Column(db.Boolean)
  
  def __init__(self,username,password):
    self.username = username
    self.password = password
    self.token = get_random_string(8)
    self.admin = False
    self.cart = ""
    self.login_attempt = 0
    self.active = True
  
  def is_active(self):
    return(self.active)

  def get_id(self):
    return(self.username)

  def is_authenticated():
    return(True) 

  def is_anonymous():
    return(False)

class Item_db(db.Model):
  __bind_key__ = 'product'
  item_id = db.Column("item_id",db.String, primary_key=True)
  price = db.Column(db.Integer)
  name = db.Column(db.String(1000))

  def __init__(self,name,price):
     self.name = name
     self.price = price
     self.item_id = get_random_string(12)

@login_manager.user_loader
def load_user(user_id):
    return Users_db.query.get(user_id)

@app.before_request
def before_request():
    user_session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=45)

login_manager.login_view = "login"
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


import frontend
import admin_main

if __name__ == "__main__":
      db.create_all()
      app.run(debug=True,ssl_context=('cert.pem', 'key.pem'))