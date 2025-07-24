from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///sasya_project.db"

db = SQLAlchemy(app)

session = session

from . import routes
