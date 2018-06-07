from flask import Flask, jsonify, send_file, make_response, request
from flask_cors import CORS
import javbus
import btsow
import db

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/preview/<id>')
def preview(id):
    db.insert_log(id)
    if db.is_exist(id):
        print('fetch from local database')
        preview = db.get_preview(id)
    else:
        print('fetch from online webpage')
        preview = javbus.get_preview(id)
        db.insert_movie(id, preview)
    return jsonify(preview)


@app.route('/log/<id>')
def log(id):
    timestamp = db.get_last_visit(id)
    return jsonify(timestamp)

@app.route('/download/<id>')
def download(id):
    download = btsow.get_download(id)
    return jsonify(download)


@app.route('/info/<id>', methods=['GET', 'POST'])
def info(id):
    if request.method == 'POST':
        genres = request.form.get['genres']
        cast = request.form.get['cast']
        db.update_info(id, genres, cast)
        print('update info of {}'.format(id))
    else:
        return jsonify(db.has_info(id))


@app.route('/content')
def content():
    res = make_response(send_file('content.html'))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


if __name__ == '__main__':
    app.run(debug=True)