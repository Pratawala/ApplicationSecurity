from flask import redirect, render_template
from flask import Flask, make_response, url_for
from flask import request, request
from flask_sqlalchemy import SQLAlchemy
from Objects.Product import Product
from Objects.User import User 
from tools.random_key import get_random_string


user_lst = {"abcde123":User("Tester123","Password123",["item1","item2","item3"],True)}
product_lst = {"item1234":Product("Shoe1",50,100,["S","M","L"]),"item1235":Product("Shoe2",60,101,["S","M"]),"item1236":Product("Shoe3",70,102,["M","L"])}
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.sqlite3'
app.config['SQLALCHEMY_BINDS'] = {'product' : 'sqlite:///product.sqlite3'}
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)

class Users_db(db.Model):
  
  username = db.Column("username",db.String, primary_key=True)
  password = db.Column(db.String(100))
  token = db.Column(db.String(100))
  admin = db.Column(db.Boolean)
  cart = db.Column(db.String(1000))
  
  def __init__(self,username,password):
    self.username = username
    self.password = password
    self.token = get_random_string(8)
    self.admin = False
    self.cart = "test,test2,test3"


class Item_db(db.Model):
  __bind_key__ = 'product'
  item_id = db.Column("item_id",db.String, primary_key=True)
  price = db.Column(db.Integer)
  name = db.Column(db.String(1000))

  def __init__(self,name,price):
     self.name = name
     self.price = price
     self.item_id = get_random_string(12)

import frontend
import admin_main

if __name__ == "__main__":
      db.create_all()
      app.run("0.0.0.0",443,debug=True) 