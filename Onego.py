from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField, TimeField, IntegerField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError, Optional
import os.path

# configuring the app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'i8f5Y2aGzn2B3Xmv9prPyEmskqZ5YVcuhwghklB0rq0VBUPc4bAvKqpPOFSQ'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

#db models
class User(UserMixin ,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique = True, nullable = False)
    forename = db.Column(db.String(120), nullable = False)
    surname = db.Column(db.String(120), nullable = False)
    gender = db.Column(db.String(1), nullable = False)
    password = db.Column(db.String(60), nullable = False)
    guardemail = db.Column(db.String(60), nullable = True)
    guardnumber = db.Column(db.String(60), nullable = True)
    DOB = db.Column(db.Date, nullable = False)
    Admin = db.Column(db.Boolean, nullable = False)
    
    def __repr__(self):
        return f"User: {self.email}, Password: {self.password}, Admin: {self.Admin}"
    
class Competitions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), nullable = False)
    weapon = db.Column(db.String(10), nullable = False)
    agegroupmax = db.Column(db.String(70), nullable = False)
    numberoffencers = db.Column(db.Integer, nullable = False)
    gender = db.Column(db.String(6), nullable = False)
    startdate = db.Column(db.Date, nullable = False, default=datetime.utcnow)
    starttime = db.Column(db.Time, nullable = False, default=datetime.utcnow)
    
    
    def __repr__(self):
        return f"Post: {self.title}, Date: {self.password}"
    
db.create_all()
#forms
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
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already in use. Please choose a different one')

class CompetitionForm(FlaskForm):
    title = StringField('Title', validators = [DataRequired()])
    agegroupmax = IntegerField('Maximum age', validators = [DataRequired()])
    weapon = SelectField('Gender', choices=[('foil','Foil'),('epee','Epee'),('sabre','Sabre')], validators = [DataRequired()])
    gender = SelectField('Gender', choices=[('M','Male'),('F','Female')], validators = [DataRequired()])
    numberoffencers = IntegerField('Maximum number of fencers', validators = [DataRequired()])
    startdate = DateField('When is it? (DD/MM/YYYY)', validators = [DataRequired()], format= '%d/%m/%Y')
    starttime = TimeField("Check in time", validators = [DataRequired()])
    submit = SubmitField('Create')
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
#login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

posts = [
    { 'author': 'Joe Smith',
      'title': 'Blog Post 1',
      'content': 'First Ever Post!!!',
      'date_posted': 'August 27, 2020'
        },
    { 'author': 'Billy Bob',
      'title' : 'Blog Post 2',
      'content': 'Second Ever Post!!!',
      'date_posted': 'August 27, 2020'
        }
]
#routes
@app.route('/')
@app.route('/home')
def HomePage():
    return render_template('home.html',title = 'Home', posts = posts)

@app.route('/about')
def AboutPage():
    return render_template('about.html',title = 'About')

@app.route('/competition_creator', methods=['GET','POST'])
@login_required
def Competition_creator():
    form = CompetitionForm()
    if current_user.Admin:
        form = CompetitionForm()
        if form.validate_on_submit():
            competition = Competitions()
            if competition:
                flash(f'You have successfully created a competition', 'success')
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('CompetitionsPage'))
        else:
            flash(f'Login unsuccessful. Please check email and password', 'danger')
        return render_template('competition_creator.html',title = 'Competition Creator')
    else:
        flash(f'You need to be an admin to create a competition', 'danger')
        return redirect(url_for('CompetitionsPage'))

@app.route('/competitions')
def CompetitionsPage():
    return render_template('competitions.html',title = 'Competitions')

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('HomePage'))
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.forename.data}, please login', 'success')
        hashed_password  = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if form.guardmobile.data == "":
            form.guardmobile.data = Null
        if form.guardemail.data == "":
            form.guardmobile.data = Null
        user = User(email = form.email.data, password = hashed_password, forename = form.forename.data, surname = form.surname.data, DOB = form.DOB.data, gender = form.gender.data, guardemail = form.guardemail.data, guardnumber = form.guardmobile.data, Admin = False)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    if form.confirm_password.errors:
        flash(f'Registration unsuccessful. One or more of the fields does not meet the requirements', 'danger')
    return render_template('register.html', title ='Register',form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('HomePage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            flash(f'You have been successfully logged in!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('HomePage'))
        else:
            flash(f'Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title ='Login',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('HomePage'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html', title ='Acount')

if __name__ == '__main__':
    c = Competitions(title = "Connor's amazing comp", weapon = "Epee", agegroupmax = 17, numberoffencers = 20, gender = "M", startdate = "2005/05/05", starttime="09:30:00")
    db.session.add(c)
    db.session.commit()
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
