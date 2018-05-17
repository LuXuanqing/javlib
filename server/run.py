from flask import Flask, jsonify, send_file, make_response
import javbus
import btsow
import db

app = Flask(__name__)


@app.route('/preview/<id>')
def preview(id):
    if db.is_exist(id):
        print('fetch from local database')
        preview = db.get_preview_by_id(id)
    else:
        print('fetch from online webpage')
        preview = javbus.get_preview(id)
        db.insert_movie(id, preview)
    # 允许跨域
    res = jsonify(preview)
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


@app.route('/download/<id>')
def download(id):
    download = btsow.get_download(id)
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