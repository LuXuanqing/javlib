from flask import Flask, jsonify, send_file, make_response, request, json
from flask_cors import CORS
import javbus
import btsow
from movie import Movie

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

    def fetch_online(movie):
        print('fetching the preview of {} from javbus...'.format(id))
        preview = javbus.get_preview(movie.id)
        movie.preview = preview
        return preview

    force = request.args.get('force', 0)
    if force:
        # 强制从javbus抓取
        preview = fetch_online(av)
    else:
        # 优先从local db中查询
        preview = av.preview
        if preview is None:
            # 如果db中没preview，从javbus抓取
            preview = fetch_online(av)
    return jsonify(preview)


@app.route('/info/<id>', methods=['POST', 'GET'])
def info(id):
    av = Movie(id)
    # check exist
    if not av.exist:
        av.create()

    if request.method == 'GET':
        info = {
            'preview': json.loads(get_preview(id).get_data().decode()),
            'download': btsow.get_download(id),  # 每次都从btsow抓取
            'genres': av.genres,
            'cast': av.cast,
            'last_visit': av.last_visit
        }
        # log
        av.log()
        return jsonify(info)
    else:
        data = json.loads(request.get_data())
        genres = data.get('genres')
        cast = data.get('cast')
        # 参数不为空时才更新数据
        if genres:
            av.genres = genres
        if cast:
            av.cast = cast
        return jsonify(success=True, genres=av.genres, cast=av.cast)


if __name__ == '__main__':
    app.run(debug=True)