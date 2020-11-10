from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError, Optional

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    forename = StringField('Forename', validators = [DataRequired()])
    surname = StringField('Surname', validators = [DataRequired()])
    guardemail = StringField('Guardian Email', validators = [Optional(), Email()])
    guardmobile = StringField('Guardian Phone Number',validators = [])
    gender = SelectField('Gender', choices=[('M','Male'),('F','Female')], validators = [DataRequired()])
    DOB = DateField('Date of Birth (DD/MM/YYYY)', validators = [DataRequired()], format= '%d/%m/%Y')
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')    