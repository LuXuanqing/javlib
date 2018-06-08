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


@app.route('/preview/<id>', methods=['POST', 'GET'])
def get_preview(id, internal=False):
    av = Movie(id)

    if request.method == 'GET':

        def fetch_online(movie):
            print('fetching the preview of {} from javbus...'.format(id))
            preview = javbus.get_preview(movie.id)
            movie.preview = preview
            return preview

        if internal:
            # 通过GET /info/<id>调用
            # 优先从local db中查询
            preview = av.preview
            if preview is None:
                # 如果db中没preview，从javbus抓取
                preview = fetch_online(av)
        else:
            # 从外部浏览器调用
            # 强制从javbus抓取
            preview = fetch_online(av)

        return jsonify(preview)
    else:
        preview = json.loads(request.get_data())
        # 只要传来的preview数据不为空，每次都会更新local db中的数据
        if preview:
            # check exist
            if not av.exist:
                av.create()
            av.preview = preview
            return jsonify(success=True)


@app.route('/info/<id>', methods=['POST', 'GET'])
def info(id):
    av = Movie(id)
    # check exist
    if not av.exist:
        av.create()

    if request.method == 'GET':
        info = {
            'preview': json.loads(get_preview(id, True).get_data().decode()),
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