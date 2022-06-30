from __main__ import app
from flask import Flask, render_template, flash
from flask import redirect, url_for, request
from flask_login import login_required
from tools.random_key import get_random_string
from main import Item_db, db, Users_db
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
  try:
    is_admin = user_session["admin"]
  except:
    return redirect(url_for("main"))
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
@login_required
def add_item():
  try:
    is_admin = user_session["admin"]
  except:
    return redirect(url_for("login"))
  if is_admin == None:
    return redirect(url_for("login"))
  elif is_admin == True:
    try:
      name = request.args.get("name")
      price = int(request.args.get("price"))
      product = Item_db(name,price)
      db.session.add(product)
      db.session.commit()
      flash("item sucessfully added")
      return redirect(url_for("manage"))
    except:
      return(redirect(url_for("manage")))
  else:
    return redirect(url_for("main"))

@app.route("/admin/api/delete_item")
@login_required
def delete_item():
  try:
    is_admin = user_session["admin"]
  except:
    return redirect(url_for("main"))
  if is_admin == None:
    return redirect(url_for("login"))
  elif is_admin == True:
    try:
      item_id = request.args.get("item_id")
      Item_db.query.filter_by(item_id=item_id).delete()
      db.session.commit()
      flash("item succesfully deleted")
      return redirect(url_for("manage"))
    except:
      return(redirect(url_for("manage")))
  else:
    return redirect(url_for("main"))

@app.route("/admin/account_manage")
@login_required
def account_manage():
  try:
    is_admin = user_session["admin"]
  except:
    return redirect(url_for("main"))
  if is_admin == None:
    return redirect(url_for("login"))
  elif is_admin == True:
    account_dict = {}
    raw_account_lst = Users_db.query.all()
    for i in raw_account_lst:
      account_dict[i.username] = [i.admin,i.token]
    return(render_template("admin/account_manage.html",account_dict=account_dict))
  else:
    return redirect(url_for("main"))