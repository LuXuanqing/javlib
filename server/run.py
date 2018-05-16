from flask import Flask, jsonify, send_file, make_response
from javbus import get_preview
from btsow import get_download

app = Flask(__name__)


@app.route('/preview/<id>')
def preview(id):
    preview = get_preview(id)
    # 允许跨域
    res = jsonify(preview)
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


@app.route('/download/<id>')
def download(id):
    download = get_download(id)
    # 允许跨域
    res = jsonify(download)
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


@app.route('/content')
def content():
    res = make_response(send_file('content.html'))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


if __name__ == '__main__':
    app.run(debug=True)