from flask import Flask, jsonify
from javbus import get_pics
from btsow import get_links

app = Flask(__name__)

@app.route('/info/<bangou>')
def info(bangou):
    pics = get_pics(bangou)
    links = get_links(bangou)
    info = {'pics': pics, 'links': links}
    # 允许跨域
    res = jsonify(info)
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


app.run(debug=True)