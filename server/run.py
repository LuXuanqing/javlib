from flask import Flask, jsonify, send_file, make_response
from javbus import get_pics
from btsow import get_links

app = Flask(__name__)


@app.route('/info/<bangou>')
def info(bangou):
    
    pics = get_pics(bangou)
    links = get_links(bangou)
    info = {'pics': pics, 'links': links}
    res = jsonify(info)
    # 允许跨域
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


@app.route('/content')
def content():
    res = make_response(send_file('content.html'))
    # 允许跨域
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


if __name__ == '__main__':
    app.run(debug=True)