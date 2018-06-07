from flask import Flask, jsonify, send_file, make_response, request
from flask_cors import CORS
import javbus
import btsow
from movie import Movie
import json

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/content')
def content():
    res = make_response(send_file('content.html'))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route('/preview/<id>')
def get_preview(id):
    av = Movie(id)
    preview = av.preview
    if preview is None:
        # 如果db中没preview，从javbus抓取
        print('fetching the preview of {} from javbus...'.format(id))
        preview = javbus.get_preview(id)
        av.preview = preview
    return jsonify(preview)


@app.route('/info/<id>')
def info(id):
    av = Movie(id)
    
    # check exist
    if not av.exist:
        av.create()

    info = {
        'preview': json.loads(get_preview(id).data.decode()),
        'download': btsow.get_download(id),  # 每次都从btsow抓取
        'genres': av.genres,
        'cast': av.cast,
        'last_visit': av.last_visit
    }

    # log
    av.log()

    return jsonify(info)


# @app.route('/info/<id>', methods=['GET', 'POST'])
# def info(id):
#     if request.method == 'POST':
#         genres = request.form.get['genres']
#         cast = request.form.get['cast']
#         db.update_info(id, genres, cast)
#         print('update info of {}'.format(id))
#     else:
#         return jsonify(db.has_info(id))

if __name__ == '__main__':
    app.run(debug=True)