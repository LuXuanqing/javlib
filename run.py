from flask import Flask, json, jsonify, send_file, make_response, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import datetime
import javbus
# import btsow
# from movie import Movie

app = Flask(__name__)
# 跨域设置
CORS(app, supports_credentials=True)
# db设置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Av(db.Model):
    id = db.Column(db.String(16), primary_key=True, index=True)
    genres = db.Column(db.String)
    casts = db.Column(db.String)
    imgs = db.Column(db.Text)
    last_updated = db.Column(db.DateTime)
    last_visited_url = db.Column(db.String)
    is_dislike = db.Column(db.Boolean)
    need_hd = db.Column(db.Boolean)

    def __repr__(self):
        return '<Av {}>'.format(self.id)


'''
POST /dislike/<id>
入参：
is_disliked: Boolean
出参：
success: Boolean

'''


# 嵌入到页面内的html内容
@app.route('/content')
def content():
    res = make_response(send_file('content.html'))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


@app.route('/preview/<id>', methods=['POST'])
def preview(id):
    '''
    入参：
    genres: json string, 分类信息
    casts: json string, 演员信息
    last_visited_url: string, 访问页面的url
    force_reload: Boolean，强制重新爬取预览图
    出参：
    imgs: json string, 预览图信息
    last_updated: DateTime,上次访问时间
    last_visited_url: String, 上次访问该片的url
    '''
    req_params = json.loads(request.get_data())
    result = {}
    try:
        # 尝试从db中获取该av，如果没有则新建
        video = Av.query.filter_by(id=id).first()
        if video is None:
            video = Av(id=id)
        #获取imgs，如果强制重载或没有数据则从javbus爬一边，否则取数据库
        if req_params.get('force_reload') or video.imgs is None:
            result['imgs'] = javbus.get_previews(id)
        else:
            result['imgs'] = video.imgs
        # 在更新之前返回上一次的last_updated,last_visited_url
        result['last_updated'] = av.last_updated
        result['last_visited_url'] = av.last_visited_url
        # 更新casts, genres
        video.casts = req_params.get('casts') or video.casts
        video.genres = req_params.get('genres') or video.genres
        # 更新last_updated,last_visited_url
        video.last_updated = datetime.datetime.now()
        video.last_visited_url = req_params.get('url')
        db.session.add(video)
        db.session.commit()
        success = True
    except Exception as err:
        # print(err)
        pass
    finally:
        return jsonify(result)



# @app.route('/preview/<id>', methods=['POST', 'GET'])
# def get_preview(id, internal=False):
#     av = Movie(id)

#     if request.method == 'GET':

#         def fetch_online(movie):
#             print('fetching the preview of {} from javbus...'.format(id))
#             preview = javbus.get_preview(movie.id)
#             movie.preview = preview
#             return preview

#         if internal:
#             # 通过GET /info/<id>调用
#             # 优先从local db中查询
#             preview = av.preview
#             if preview is None:
#                 # 如果db中没preview，从javbus抓取
#                 preview = fetch_online(av)
#         else:
#             # 从外部浏览器调用
#             # 强制从javbus抓取
#             preview = fetch_online(av)

#         return jsonify(preview)
#     else:
#         # 这里是从javbus POST preview信息，同时获取last visit
#         preview = json.loads(request.get_data())
#         # 只要传来的preview数据不为空，每次都会更新local db中的数据
#         if preview:
#             # check exist
#             if not av.exist:
#                 av.create()
#             av.preview = preview
#         # log
#         av.log('javbus')
#         last_visit = json.loads(get_last_visit(id).get_data().decode())
#         return jsonify(success=True,last_visit=last_visit)

# @app.route('/log/<id>')
# def get_last_visit(id):
#     av = Movie(id)
#     data = av.last_visit
#     return jsonify(data)

# @app.route('/info/<id>', methods=['POST', 'GET'])
# def info(id):
#     av = Movie(id)
#     # check exist
#     if not av.exist:
#         av.create()

#     if request.method == 'GET':
#         info = {
#             'preview': json.loads(get_preview(id, True).get_data().decode()),
#             'download': btsow.get_download(id),  # 每次都从btsow抓取
#             'genres': av.genres,
#             'cast': av.cast,
#             'last_visit': json.loads(get_last_visit(id).get_data().decode())
#         }
#         # log
#         av.log('javlib')
#         return jsonify(info)
#     else:
#         data = json.loads(request.get_data())
#         genres = data.get('genres')
#         cast = data.get('cast')
#         # 参数不为空时才更新数据
#         if genres:
#             av.genres = genres
#         if cast:
#             av.cast = cast
#         return jsonify(success=True, genres=av.genres, cast=av.cast)

if __name__ == '__main__':
    app.run(debug=True)