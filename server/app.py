from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user,login_required
import os

database_path = "../instance/data.db"
app = Flask(__name__)
app.config['SECRET_KEY'] = "itsverysecret"
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{database_path}"


db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

