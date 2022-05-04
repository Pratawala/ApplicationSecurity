from flask import redirect, render_template
from flask import Flask, make_response, url_for
from flask import request, request 

user_lst = {"abcde123":{"username":"Tester123","password":"Password123"}}

app = Flask(__name__)

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
    if user_lst[user]["username"] == username:
      current_user = user
      break
  try: 
    if password == user_lst[current_user]["password"]:
      token = "abcde123"
      response = make_response(redirect(url_for("main")))
      response.set_cookie('token', token, max_age=60*60*12)
      return response
    else:
      return render_template("/frontend/login_fail.html")
  except:
    return render_template("/frontend/login_fail.html")
@app.route("/signup/create",methods=["GET","POST"])
def create_account():
  print(request.form.get("username"))
  return render_template("/frontend/homepage.html")

if __name__ == "__main__":
    app.run("0.0.0.0",443,debug=True)  
    
