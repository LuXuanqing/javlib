from flask import Flask, jsonify
from javbus import get_pics

app = Flask(__name__)

@app.route('/info/<bangou>')
def info(bangou):
    pics = get_pics(bangou)
    res = jsonify(pics)
    # 允许跨域
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


app.run(debug=True)