from flask import Flask, jsonify
from javbus import get_pics

app = Flask(__name__)

@app.route('/info/<bango>')
def info(bango):
    pics = get_pics(bango)
    res = jsonify(pics)
    # 允许跨域
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


app.run(debug=True)