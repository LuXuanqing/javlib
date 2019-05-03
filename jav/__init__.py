from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask('jav')
app.config.from_pyfile('settings.py')

db = SQLAlchemy(app)
# 下面这些参数好像没什么用，依然要在每个请求的response里面手动设置。另外用@app.after_request统一修改res header似乎也没用
cors = CORS(app, origins='*', expose_headers='*', allow_headers='*')

from jav import views, errors, commands
