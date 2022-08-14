from __main__ import app
from flask import render_template
from flask import redirect, url_for
from flask_login import login_required
from main import db, Users_db
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
