from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,TextAreaField,PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo

from flask_wtf.file import FileField, FileAllowed,FileRequired


class SignupForm(FlaskForm):
    fullname = StringField("Fullname",validators=[DataRequired(message="your fullname is required.")])
    email = StringField("Email",validators=[Email()])
    password =PasswordField("password", validators=[DataRequired()])

    confirm_password = PasswordField("confirm password",validators=[EqualTo('password',message="Confirm password must be equal to password")])

    btn = SubmitField("sign up!")

class ProfileForm(FlaskForm):
    fullname = StringField("Fullname",validators=[DataRequired(message="your fullname is required.")])
    pix =FileField('Display Picture', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Image only!')])
    btn = SubmitField("Update profile")
 
  
    
    
    
    
    
     
    

