from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
import os

app=Flask(__name__)
app.config.from_object('config')

lm = LoginManager()
lm.setup_app(app)
lm.login_view = "unauthorized"


db = SQLAlchemy(app)

from app import models,views
