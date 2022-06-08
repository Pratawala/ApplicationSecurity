from flask import Flask, redirect, url_for, render_template, request
from main import Users_db

def admin_check(db):
  try:
    token = request.cookies.get("token")
    admin_check = db.session.query(Users_db).filter_by(token=token).first()
    admin_check = admin_check.admin
  except:
    return None
  if admin_check == True:
    return True
  else:
    return False