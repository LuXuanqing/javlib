from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask('jav')
app.config.from_pyfile('settings.py')

db = SQLAlchemy(app)

from jav import views, errors, commands
