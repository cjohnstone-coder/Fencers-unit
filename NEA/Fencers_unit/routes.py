from flask import render_template, url_for, flash, redirect
from Fencers_unit.forms import RegistrationForm, LoginForm
from Fencers_unit import app, bcrypt, db
from Fencers_unit.models import User, Competitions
from flask_login import login_user
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
@app.route('/')
@app.route('/home')
def HomePage():
    return render_template('home.html',title = 'Home', posts = posts)

@app.route('/about')
def AboutPage():
    return render_template('about.html',title = 'About')

@app.route('/competitions')
def CompetitionsPage():
    return render_template('competitions.html',title = 'Competitions')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.forename.data}, please login', 'success')
        hashed_password  = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if form.guardmobile.data == "":
            form.guardmobile.data = Null
        user = User(email = form.email.data, password = hashed_password, forename = form.forename.data, surname = form.surname.data, DOB = form.DOB.data, gender = form.gender.data, guardemail = form.guardemail.data, guardnumber = form.guardmobile.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    if form.confirm_password.errors:
        flash(f'Registration unsuccessful. One or more of the fields does not meet the requirements', 'danger')
    return render_template('register.html', title ='Register',form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            flash(f'You have been successfully logged in!', 'success')
            return redirect(url_for('HomePage'))
        else:
            flash(f'Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title ='Login',form=form)