from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = "itsverysecret"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"


db = SQLAlchemy(app)