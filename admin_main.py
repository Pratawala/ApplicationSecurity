from __main__ import app
from flask import Flask, render_template, flash
from flask import redirect, url_for, request
from flask_login import login_required
from requests import session
from Objects.Product import Product
from Objects.User import User
from tools.admin_check import admin_check 
from tools.random_key import get_random_string
from main import Item_db, db,product_lst, Users_db
from flask import session as user_session

@app.route("/make_admin")
@login_required
def make_admin():
  token = user_session["token"]
  exists = db.session.query(Users_db.token).filter_by(token=token).first() is not None #testing purposes only
  if exists == True:
    current_user = db.session.query(Users_db).filter_by(token=token).first()
    current_user.admin = True
    db.session.commit()
    user_session["admin"] = current_user.admin
  return(redirect(url_for("main")))
@app.route("/admin")
@login_required
def main_admin(): 
  is_admin = user_session["admin"]
  if is_admin == None:
    return redirect(url_for("login"))
  elif is_admin == True:
    return render_template("/admin/homepage.html")
  elif is_admin == False:
    return redirect(url_for("main"))
@app.route("/admin/manage")
@login_required
def manage():
  product_lst = []
  is_admin = user_session["admin"]
  if is_admin == None:
    return redirect(url_for("login"))
  elif is_admin == True:
    object_product_lst = Item_db.query.all()
    for item in object_product_lst:
      product_lst.append({"item_id":item.item_id,"price":item.price,"name":item.name})
    return render_template("/admin/manage.html",product_lst=product_lst)
  elif is_admin == False:
    return redirect(url_for("main"))

@app.route("/admin/api/add_item")
def add_item():
  is_admin = user_session["admin"]
  if is_admin == None:
    return redirect(url_for("login"))
  elif is_admin == True:
    name = request.args.get("name")
    price = request.args.get("price")
    product = Item_db(name,price)
    db.session.add(product)
    db.session.commit()
    flash("item sucessfully added")
    return redirect(url_for("manage"))
  else:
    return redirect(url_for("main"))