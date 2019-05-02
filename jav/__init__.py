from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask('jav')
app.config.from_pyfile('settings.py')

db = SQLAlchemy(app)
cors = CORS(app)

from jav import views, errors, commands