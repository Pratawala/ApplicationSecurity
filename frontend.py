from asyncio.windows_events import NULL
from flask import redirect, render_template
from flask import Flask, make_response, url_for
from flask import request, request, flash
from sqlalchemy import false
from Objects.Product import Product
from Objects.User import User
from tools.random_key import get_random_string
import json
from __main__ import app
from main import product_lst, user_lst, Users_db, db, Item_db

@app.route("/")
def main():
    product_dict = Item_db.query.all()
    return render_template('/frontend/homepage.html',products_lst=product_dict)

@app.route("/login")
def login():
  return render_template('frontend/login.html')

@app.route("/signup")
def signup():
  return render_template("/frontend/signup.html",error="")
    
@app.route("/login/signin",methods=["GET","POST"])
def signin():
  current_user = ""
  username = request.form.get("username")
  password = request.form.get("password")
  exists = db.session.query(Users_db.username).filter_by(username=username).first() is not None
  if exists == True:
    current_user = Users_db.query.get(username)
    if current_user.password == password: 
      current_user.token = get_random_string(8)
      db.session.commit()
      token = current_user.token
      response = make_response(redirect(url_for("main")))
      response.set_cookie('token', token, max_age=60*60*24) #create cookie, set cookie to expire after 24h(60s x 60m x 24h)
      return response
    else:
      return render_template("/frontend/login_fail.html")
  return render_template("/frontend/login_fail.html")
@app.route("/signup/create",methods=["GET","POST"])
def create_account():
  exists = False
  try:
    new_username = request.form.get("username")
    new_password = request.form.get("password")
    exists = db.session.query(Users_db.username).filter_by(username=new_username).first() is not None
    if exists == True:
      flash('Username already exists')
      return redirect(url_for("signup"))
    new_user = Users_db(new_username,new_password)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("login"))
  except:
    return redirect(url_for("/500"))

@app.route("/api/getcart")
def get_cart():
  try:
    token = request.args.get("token")
    exists = db.session.query(Users_db.token).filter_by(token=token).first() is not None
    if exists == True:
      current_user = db.session.query(Users_db).filter_by(token=token).first()
      user_cart = current_user.cart
      return {"usercart":user_cart}
    elif token == None or token == "" or token == NULL:
      response = make_response(redirect(url_for("login")))
      return response
    else:
      return redirect(url_for("internal_server_error"))
  except:
    return redirect(url_for("/internal_server_error"))

@app.route("/cart")
def cart():
    token = request.cookies.get("token")
    exists = db.session.query(Users_db.token).filter_by(token=token).first() is not None
    if exists == True:
      current_user = db.session.query(Users_db).filter_by(token=token).first()
      user_cart = current_user.cart
      return render_template("frontend/cart.html",user_cart=user_cart)
    elif token == None or token == "" or token == NULL:
      response = make_response(redirect(url_for("login")))
      return response
    else:
      return redirect(url_for("internal_server_error"))
    
@app.route("/500")
def internal_server_error():
  return render_template("frontend/error500.html")

@app.route("/productPage")
def product_page():
  item_id = request.args.get("item_id")
  ##product = Item_db("hello",50)
  ##db.session.add(product)
  ##db.session.commit()
  product_info = Item_db.query.get(item_id)
  product_info_lst = [product_info.name,product_info.price]
  return render_template("frontend/productPage.html",product_info=product_info_lst)