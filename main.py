from asyncio.windows_events import NULL
from flask import redirect, render_template
from flask import Flask, make_response, url_for
from flask import request, request
from Objects.User import User 
from tools.random_key import get_random_string

user_lst = {"abcde123":User("Tester123","Password123",["item1","item2","item3"],True)}
app = Flask(__name__)
          
@app.route("/admin")
def main_admin():
    try:
      token = request.cookies.get("token")
      admin_check = user_lst[token].get_admin()
    except:
      return redirect(url_for("login"))
    if admin_check == True:
      return render_template('/admin/homepage.html')
    else:
      return redirect(url_for("main"))

@app.route("/")
def main():
    return render_template('/frontend/homepage.html')

@app.route("/login")
def login():
  return render_template('frontend/login.html')

@app.route("/signup")
def signup():
  return render_template("/frontend/signup.html")
    
@app.route("/login/signin",methods=["GET","POST"])
def signin():
  current_user = ""
  username = request.form.get("username")
  password = request.form.get("password")
  for user in user_lst:
    if user_lst[user].get_username() == username:
      current_user = user
      break
  try: 
    if password == user_lst[current_user].get_password():
      token = current_user
      response = make_response(redirect(url_for("main")))
      response.set_cookie('token', token, max_age=60*60*12) #create cookie, set cookie to expire after 12h(60s x 60m x 12h)
      return response
    else:
      return render_template("/frontend/login_fail.html")
  except:
    return render_template("/frontend/login_fail.html")
@app.route("/signup/create",methods=["GET","POST"])
def create_account():
  try:
    new_username = request.form.get("username")
    new_password = request.form.get("password")
    key = get_random_string(8)
    user_lst[key] = User(new_username,new_password,[],False)
    return redirect(url_for("login"))
  except:
    return redirect(url_for("/500"))

@app.route("/api/getcart")
def get_cart():
  try:
    token = request.args.get("token")
    if token in user_lst:
      user_cart = user_lst[token].get_cart()
      print(user_cart)
      return {"usercart":user_cart}
    elif token == None or token == "" or token == NULL:
      response = make_response(redirect(url_for("login")))
      return response
    else:
      return redirect(url_for("/500"))
  except:
    return redirect(url_for("/500"))

@app.route("/cart")
def cart():
  try:
    token = request.cookies.get("token")
    if token in user_lst:
      user_cart = user_lst[token].get_cart()
      return render_template("frontend/cart.html")
    else:
      return redirect(url_for("login"))
  except:
    return redirect(url_for("internal_server_error"))

if __name__ == "__main__":
      app.run("0.0.0.0",443,debug=True)  
    
@app.route("/500")
def internal_server_error():
  return render_template("frontend/error500.html")