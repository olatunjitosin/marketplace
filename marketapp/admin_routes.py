import re,random,os
from flask import render_template, request, redirect, flash,make_response,session,url_for
from sqlalchemy.sql import text
from marketapp import app, csrf
from marketapp.models import db,Admin,Category






@app.route("/admin/login/", methods=["GET","POST"])
def adminlogin():
    if request.method =="GET":
        return render_template("/admin/login.html")
    else:
        username=request.form.get("username")
        pwd=request.form.get("password")

        chk=db.session.query(Admin).filter(Admin.admin_username == username,Admin.admin_pwd == pwd).count()
        #.all(), if all() contains smt, it will give you a list, if it doesnt, it will give an empty list
        if chk:
            session['admin_loggedin']=True
            return redirect("/admin/dashboard")
        else:
            flash("incorrect credentials")
            return redirect("/admin/login/")



        
@app.route("/admin/logout")
def admin_logout():
    if session.get("admin_loggedin"):
        session.pop("admin_loggedin", None)
        flash("You have logged out succesfully....")
    return redirect ("/admin/login")
    


@app.route("/admin/dashboard/")
def adminhome():
    return render_template("admin/admin_dashboard.html")
