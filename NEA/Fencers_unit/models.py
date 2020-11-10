from Fencers_unit.__init__ import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
@login_manager.header_loader
def load_user_from_header(header_val):
    header_val = header_val.replace('Basic ', '', 1)
    try:
        header_val = base64.b64decode(header_val)
    except TypeError:
        pass
    return User.query.filter_by(api_key=header_val).first()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique = True, nullable = False)
    forename = db.Column(db.String(120), nullable = False)
    surname = db.Column(db.String(120), nullable = False)
    gender = db.Column(db.String(1), nullable = False)
    password = db.Column(db.String(60), nullable = False)
    guardemail = db.Column(db.String(60), nullable = True)
    guardnumber = db.Column(db.String(60), nullable = True)
    DOB = db.Column(db.Date, nullable = False)
    
    def __repr__(self):
        return f"User: {self.email}, Password: {self.password}"
    
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