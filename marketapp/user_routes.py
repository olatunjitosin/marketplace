import re,random,os
from functools import wraps
from flask import render_template, request, redirect, flash,make_response,session,url_for
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash,check_password_hash
from marketapp import app, csrf
from marketapp.models import db,User



from marketapp.forms import SignupForm,ProfileForm


@app.route("/home")
def home():
    return render_template("user/home.html")

@app.route("/login/",methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template("user/login.html")
    else:
        #we are using the below method because we are using non flask form
        username=request.form.get('email')#give form input name='email'
        password=request.form.get('password')#give form input name='password'
        deets=db.session.query(User).filter(User.user_email==username).first()#will give <userid> an object
        if deets:
            hashedpwd=deets.user_pwd
            chk=check_password_hash(hashedpwd,password)#Returns True/False
            if chk:
                session['user_loggedin']=True
                session['user_id']=deets.user_id
                return redirect ("/dashboard")
            else:
                flash("Invalid Password")
                return redirect ("/login")
        else:
            flash("Invalid Username")
            return redirect ("/login")



@app.route("/layout")
def layout():
    return render_template("user/layout.html")


@app.route("/contact")
def contact():
    return render_template("user/contactus.html")





@app.route("/register/",methods=['GET','POST'])
def register():
         signupform=SignupForm()
         if request.method=='GET':
            return render_template("user/signup.html",signupform=signupform)
         else:
            if signupform.validate_on_submit():
                userpass=request.form.get('password')
                useremail=request.form.get('email')
                username=request.form.get('fullname')
                hashedpwd=generate_password_hash(userpass)

                u=User(user_fullname=username,user_email=useremail,user_pwd=hashedpwd, )
                db.session.add(u)
                db.session.commit()
                #log the user in and redirect to dashboard
                session['user_id']=u.user_id
                session['user_loggedin']=True
                flash ("You signed up Sucessfully")
                return redirect("/dashboard")
            else:
                return render_template("/user/signup.html", signupform=signupform)
            

@app.route("/about")
def about():
    return render_template("user/aboutus.html")

@app.route("/profile/",methods=['GET','POST'])
def profile():
    pform=ProfileForm()
    useronline=session.get('user_id')
    userdeets=db.session.query(User).get(useronline)
    if request.method=='GET':
      
        return render_template("user/profile.html",pform=pform,userdeets=userdeets)   
    else:
        if pform.validate_on_submit():
            fullname=request.form.get('fullname')#pform.fullname.data
            picture=request.files.get('pix')#pform.pix.filename
            filename=pform.pix.data.filename
            picture.save("bookapp/static/images/profile/"+filename)
            userdeets.user_fullname=fullname #userdeets.user_pwd=hash of what is comming iin
            userdeets.user_pix=filename
            db.session.commit()
            flash("Profile updated")
            return redirect("/dashboard")
        else:
            return render_template("user/profile.html",pform=pform,userdeets=userdeets)   
        

def login_required(f):
    @wraps(f)  #from functools import wraps
    def login_decorator(*args,**kwargs): #"**kwargs" keyworded argument for unpacking dictionary,*args for unpacking a list
        if session.get("user_id") and session.get('user_loggedin'):
           return f(*args,**kwargs)
        else:
            flash("Access Denied, Please login")
            return redirect ("/login")
    return login_decorator



@app.route("/dashboard")
@login_required
def dashboard():
    useronline=session.get('user_id')
    userdeets=db.session.query(User).get(useronline)
    return render_template("user/dashboard.html",userdeets=userdeets)







