from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from jav import config

app = Flask(__name__)
if app.env == 'development':
    app.config.from_object(config.DevelopmentConfig)
else:
    app.config.from_object(config.ProductionConfig)

db = SQLAlchemy(app)
from jav import views, commands
