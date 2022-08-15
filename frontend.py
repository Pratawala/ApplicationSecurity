from asyncio.windows_events import NULL
from flask import redirect, render_template
from flask import Flask, make_response, url_for
from flask import request, request, flash
from flask import session as user_session
from flask_login import login_required, login_user
from tools.random_key import get_random_string
from __main__ import app
from main import Users_db, db, Item_db, bcrypt, Cart_db, key,ciphertext_file,MyAes
import pickle
import json
import re
from json import JSONEncoder

@app.route("/")
def main():
  return render_template('/frontend/homepage.html')

@app.route("/login")
def login():
  return render_template('frontend/login.html')


@app.route("/signup")
def signup():
  return render_template("/frontend/signup.html",error="")
    

@app.route("/login/signin",methods=["GET","POST"])
def signin():
  regex_for_sanitaisation= ("^[A-Za-z0-9]*$")
  sanitise = re.compile(regex_for_sanitaisation)

  current_user = ""
  try: 
    username = request.form.get("username")
    if  (re.search(sanitise, username)):
        pass
    else:
        return render_template("/frontend/login_fail.html")


    password = request.form.get("password")
    exists = db.session.query(Users_db.username).filter_by(username=username).first() is not None

  except:
    return(redirect(url_for("login")))


  if exists == True:
    current_user = Users_db.query.get(username)

    if current_user.login_attempt > 3:
      # flash("Login too many times, account has been deactivated")
      current_user.active = False
      db.session.commit()
      
      return render_template("/frontend/account_locked.html")

    if bcrypt.check_password_hash(current_user.password,password): 
      login_user(current_user)
      current_user.token = get_random_string(8)
      current_user.login_attempt = 0
      db.session.commit()
      user_session["token"] = current_user.token
      user_session["admin"] = current_user.admin
      response = redirect(url_for("main"))
      ##response.set_cookie('token', token, max_age=60*60*24) #create cookie, set cookie to expire after 24h(60s x 60m x 24h)
      return response

    else:
      current_user.login_attempt += 1
      db.session.commit()
      flash(f"Login failed Atteps reamining: {3-current_user.login_attempt}")
      return redirect(url_for("login"))
  return redirect(url_for("login"))


@app.route("/signup/create",methods=["GET","POST"])
def create_account():
  flash("")

  # ReGex to check if a string
    # contains uppercase, lowercase
    # special character & numeric value
  regex_for_policy = ("^(?=.*[a-z])(?=." +
            "*[A-Z])(?=.*\\d)" +
            "(?=.*[-+_!@#$%^&*., ?]).+$")
  
  regex_for_sanitaisation= ("^[A-Za-z0-9]*$")
  p = re.compile(regex_for_policy)
  sanitise = re.compile(regex_for_sanitaisation)


  exists = False
  try:
    new_username = request.form.get("username")
    if(re.search(sanitise, new_username)):
        pass
    else:
        flash("User name can only contain Latin alphabet (A-Z or a-z) and Numbers (0-9)")
        return redirect(url_for("signup"))
 #input sanitaisation 
     

    new_password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    # for j in range(len(confirm_password)): #input sanitaisation 
    #   if confirm_password[j] in reject:
    #     flash('Password is too common') #security through obscurity (conceal input sanitaisation process)
    #     return redirect(url_for("signup"))
    

    exists = db.session.query(Users_db.username).filter_by(username=new_username).first() is not None #queries database for username

    if exists == True:
      flash('Username already exists')
      return redirect(url_for("signup"))

    if new_password != confirm_password:
      flash("Passwords do not match")
      return redirect(url_for("signup"))

    if len(new_username) > 25 or len(new_username) < 8:
      flash('Username length should be within 8-25 characters')
      return redirect(url_for("signup"))

    if len(new_password) > 64 or len(new_password) < 8:
      flash('Password length should be within 8-64 characters')
      return redirect(url_for("signup"))

    if new_password == new_username:
      flash('Password cannot be same as username!')
      return redirect(url_for("signup"))

    common = ["P@ssword123","Pa$$word123","Qwerty@123", new_username+"@123", "P@$$word123"]
    for i in range(len(common)):
      if common[i] == new_password:
        flash('password should not be commonly used ') #security through obscurity (conceal input sanitaisation process)
        return redirect(url_for("signup"))
     


    if(re.search(p, new_password)):
        pass
    else:
        flash("Password should contain at least one: special character, number from 0-9 and upper/lowercase letter ")
        return redirect(url_for("signup"))

    new_password_hash = bcrypt.generate_password_hash(new_password) #hashing password
    new_user = Users_db(new_username,new_password_hash) #entering user's username and hashed password
    db.session.add(new_user)
    db.session.commit() 
    return redirect(url_for("login")) 

  except:
    #pass
    return redirect(url_for("internal_server_error")) # please only enable pass in production

# @app.route("/api/getcart")
# def get_cart():
#   try:
#     token = user_session["token"]
#     exists = db.session.query(Users_db.token).filter_by(token=token).first() is not None
#     if exists == True:
#       current_user = db.session.query(Users_db).filter_by(token=token).first()
#       user_cart = current_user.cart
#       return {"usercart":user_cart}
#     elif token == None or token == "" or token == NULL:
#       response = make_response(redirect(url_for("login")))
#       return response
#     else:
#       return redirect(url_for("internal_server_error"))
#   except:
#     return redirect(url_for("/internal_server_error"))

@app.route("/cart")
@login_required
def cart():
    cart = Cart_db("shinshin","","")
    serialized = pickle.dumps(cart)
    filename = "cart.file"
    with open(filename, "wb") as file_object:
      file_object.write(serialized)
    with open(filename, "rb") as file_object:
      raw_data = file_object.read()
    deserialized_data = pickle.loads(raw_data)
    token = user_session["token"]
    exists = db.session.query(Users_db.token).filter_by(token=token).first() is not None
    if exists == True:
      raw_username = Users_db.query.filter_by(token=token).first()
      username = raw_username.username
      current_user_cart_obj = Cart_db.query.filter_by(username=username).all()
      current_user_cart = []
      for i in current_user_cart_obj:
        item = Item_db.query.get({i.item_id})
        current_user_cart.append([item.name,item.price,i.quantity,i.item_id])
      return render_template("frontend/cart.html",user_cart=current_user_cart,deserialized_data=deserialized_data.username)
    elif token == None or token == "" or token == NULL:
      response = make_response(redirect(url_for("login")))
      return response
    else:
      return redirect(url_for("internal_server_error"))
    
    
@app.route("/cart/api/add_to_cart")
@login_required
def add_to_cart():
  try:
    token = user_session["token"]
    cart_item = request.args.get("item_id")
    quantity = request.args.get("quantity")
    quantity = int(quantity)
    exists = db.session.query(Users_db.token).filter_by(token=token).first() is not None
    exists2 = db.session.query(Item_db.item_id).filter_by(item_id=cart_item).first() is not None
    if exists == True and exists2 == True:
      raw_username = Users_db.query.filter_by(token=token).first()
      username = raw_username.username
      new_item = Cart_db(username,cart_item,quantity)
      db.session.add(new_item)
      db.session.commit()
    return(redirect(url_for("cart")))
  except:
    return redirect(url_for("internal_server_error"))

@app.route("/cart/api/remove_from_cart")
@login_required
def remove_from_cart():
    try:
      token = user_session["token"]
      item_id = request.args.get("item_id")
      quantity_deleted = request.args.get("quantity")
      quantity_deleted = int(quantity_deleted)
      exists = db.session.query(Users_db.token).filter_by(token=token).first() is not None
      exists2 = db.session.query(Item_db.item_id).filter_by(item_id=item_id).first() is not None
      exists3 = db.session.query(Cart_db.item_id).filter_by(item_id=item_id).first() is not None
    except:
      return(redirect(url_for("internal_server_error")))
    if exists == True and exists2 == True and exists3 == True:
      raw_username = Users_db.query.filter_by(token=token).first()
      username = raw_username.username
      cart_item = Cart_db.query.filter_by(username=username,item_id=item_id).first()
      if (cart_item.quantity - quantity_deleted) <= 0:
        db.session.delete(cart_item)
      else:
        cart_item.quantity -= quantity_deleted
      db.session.commit()
    return(redirect(url_for("cart")))

@app.route("/500")
def internal_server_error():
  return render_template("frontend/error500.html")

@app.route("/productPage")
def product_page():
  try:
    product_info_lst = []
    product_lst = Item_db.query.all()
    for i in product_lst:
      product_info_lst.append([i.name,i.price,i.item_id])
    return render_template("frontend/productPage.html",product_info=product_info_lst)
  except:
    return redirect(url_for("internal_server_error"))

@app.route("/api/add_card",methods=["GET","POST"])
@login_required
def add_card():
      # encode plaintext, then encrypt
  try:
    card_detail = request.form.get("card_number")
    card_expiry_date = request.form.get("expiry_date")
    card_cvv = request.form.get("cvv")
    token = user_session["token"]
    exists = db.session.query(Users_db.token).filter_by(token=token).first() is not None
    if exists == True:
      current_user = Users_db.query.filter_by(token=token).first()
      ciphertext = MyAes.encrypt(key, card_detail.encode("utf8"))
      expiry_date_ciphertext = MyAes.encrypt(key, card_expiry_date.encode("utf8"))
      cvv_ciphertext = MyAes.encrypt(key, card_cvv.encode("utf8"))
      current_user._Users_db__card_number = ciphertext
      current_user._Users_db__cvv = cvv_ciphertext
      current_user._Users_db__card_expiry_date = expiry_date_ciphertext
      db.session.commit()
  except:
    return(redirect(url_for("internal_server_error")))
    # decrypt ciphertext, then decode
  return(redirect(url_for("main")))
@app.route("/card_details")
@login_required
def card_details():
  try:
    token = user_session["token"]
    exists = db.session.query(Users_db.token).filter_by(token=token).first() is not None
    if exists == True:
      current_user = Users_db.query.filter_by(token=token).first()
      ciphertext = current_user._Users_db__card_number
      cvv_ciphertext = current_user._Users_db__cvv
      expiry_date_ciphertext = current_user._Users_db__card_expiry_date
      if ciphertext == "" or cvv_ciphertext == "" or expiry_date_ciphertext == "":
        return(render_template("frontend/card_details.html"))
      decryptedtext_string = MyAes.decrypt(key, ciphertext).decode("utf8")
      decryptedtext_string_cvv = MyAes.decrypt(key, cvv_ciphertext).decode("utf8")
      decryptedtext_string_expiry_date = MyAes.decrypt(key, expiry_date_ciphertext).decode("utf8")
      return(render_template("frontend/card_details.html",card_details=[decryptedtext_string,decryptedtext_string_cvv,decryptedtext_string_expiry_date]))
  except:
    return(redirect(url_for("internal_server_error")))
   

