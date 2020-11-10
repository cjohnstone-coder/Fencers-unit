from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os.path

app = Flask(__name__)

app.config['SECRET_KEY'] = 'i8f5Y2aGzn2B3Xmv9prPyEmskqZ5YVcuhwghklB0rq0VBUPc4bAvKqpPOFSQ'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

import Fencers_unit.forms
import Fencers_unit.routes



