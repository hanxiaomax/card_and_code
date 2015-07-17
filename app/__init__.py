from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
import os
import logging

app=Flask(__name__)
app.config.from_object('config')

lm = LoginManager()
lm.setup_app(app)
lm.login_view = "unauthorized"

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
handler = logging.FileHandler('debug.log')
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

db = SQLAlchemy(app)

from app import models,views
