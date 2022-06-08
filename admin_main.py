from __main__ import app
from flask import Flask, render_template
from flask import redirect, url_for, request
from Objects.Product import Product
from Objects.User import User
from tools.admin_check import admin_check 
from tools.random_key import get_random_string
from main import db,product_lst, Users_db

@app.route("/make_admin")
def make_admin():
  token = request.cookies.get("token")
  exists = db.session.query(Users_db.token).filter_by(token=token).first() is not None #testing purposes only
  if exists == True:
    current_user = db.session.query(Users_db).filter_by(token=token).first()
    current_user.admin = True
    db.session.commit()
@app.route("/admin")
def main_admin(): 
  is_admin = admin_check(db)
  if is_admin == None:
    return redirect(url_for("login"))
  elif is_admin == True:
    return render_template("/admin/homepage.html")
  elif is_admin == False:
    return redirect(url_for("main"))
@app.route("/admin/manage")
def manage():
  is_admin = admin_check(db)
  if is_admin == None:
    return redirect(url_for("login"))
  elif is_admin == True:
    return render_template("/admin/manage.html",product_lst=product_lst)
  elif is_admin == False:
    return redirect(url_for("main"))