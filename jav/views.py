from flask import render_template, send_file, make_response
from jav import app, db
from jav.models import Av, History


@app.route('/content')
def content():
    res = make_response(send_file('templates/content.html'))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res
