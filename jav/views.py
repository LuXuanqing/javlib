from flask import request, send_file, make_response, jsonify
from jav import app, db
from jav.models import Av, History
from jav import bots
from jav.log import create_logger

logger = create_logger(__name__)


# utils
def handle_response(res):
    """
    为response加上允许跨域
    """
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


def fetch_av(id):
    # 从数据库查询，没有则新建
    av = Av.query.get(id)
    if not av:
        av = Av(id=id)
        db.session.add(av)
        db.session.commit()
        logger.info('Inserted av {}.'.format(av))
    return av


def get_imgs_from_av(av):
    # 如果没有图片，从网上爬
    if av.imgs_ is None:
        imgs = bots.get_previews(av.id)
        if imgs:
            av.imgs_ = imgs
            db.session.commit()
            logger.info('Updated imgs of {}'.format(av))
    return av.imgs_


def access_log(id, referer=None):
    """
    获取上次访问信息，并添加这次访问信息
    :param id:
    :return: 上次访问信息<History>
    """
    last_visit = History.query.filter_by(av_id=id).order_by(History.timestamp.desc()).first()
    # 记录这次访问
    # TODO 写入访问历史（最好可以通过fetch_av来创建）
    # TODO 用装饰器做成每次请求后自动添加访问记录
    this_visit = History(av_id=id, site=request.referrer or referer)
    db.session.add(this_visit)
    db.session.commit()
    logger.info('Insert AccessLog {}'.format(this_visit))
    return last_visit


def update_info(av, data):
    """
    检查av中是否有genres, casts信息，如果没有则更新
    :param av:
    :param data:
    :return:
    """
    is_changed = False
    if av.genres_ is None and data.get('genres'):
        av.genres_ = data['genres']
        is_changed = True
    if av.casts_ is None and data.get('casts'):
        av.casts_ = data['casts']
        is_changed = True
    # 如果更新了，则写入数据库
    if is_changed:
        db.session.commit()
        logger.info('Updated info of {}'.format(av))


# views
@app.route('/content/<name>')
def content(name):
    if name == 'javlib':
        res = make_response(send_file('templates/javlib.html'))
    elif name == 'javbus':
        res = make_response(send_file('templates/javbus.html'))
    else:
        return 'invalid content name', 404
    return handle_response(res)


# javbus: post imgs
# all: put dislike, needhd; last visit

@app.route('/api/javlib/<id>', methods=['POST'])
def javlib(id):
    """
    更新genres, casts，并获取imgs, 上次访问
    :param id: av的番号，例如SSNI-413
    :param genres: 类别，list
    :param casts: 演员，list
    :return:
    """
    av = fetch_av(id)
    last_visit = access_log(id)

    data = request.get_json()
    update_info(av, data)

    res = make_response(jsonify({
        'imgs': get_imgs_from_av(av),
        'lastVisit': {
            'timestamp': last_visit.timestamp if last_visit else None,
            'site': last_visit.site if last_visit else None
        },
        'isDislike': av.is_dislike,
        'isNeedHd': av.is_need_hd
    }))
    return handle_response(res)


@app.route('/api/javbus/<id>', methods=['POST'])
def javbus(id):
    av = fetch_av(id)
    last_visit = access_log(id, referer='https://www.javbus.com')
    data = request.get_json()
    imgs = data.get('imgs')
    # TODO 错误检验
    # 如果av没有imgs，并且post的data中有imgs，则写入数据库
    if av.imgs_ is None and imgs:
        av.imgs_ = imgs
        db.session.commit()
        logger.info('Updated imgs of {}'.format(av))
    res = make_response(jsonify({
        'lastVisit': {
            'timestamp': last_visit.timestamp if last_visit else None,
            'site': last_visit.site if last_visit else None
        },
        'isDislike': av.is_dislike,
        'isNeedHd': av.is_need_hd
    }))
    return handle_response(res)


@app.route('/api/av/<id>/imgs')
def get_imgs(id):
    av = fetch_av(id)
    # TODO 如果返回数据为空，应该不是200
    return jsonify(get_imgs_from_av(av))


@app.route('/api/av/<id>/dislike', methods=['PUT'])
def av_dislike(id):
    """更新is dislike,request body中isDislike需要为布尔值"""
    is_dislike = request.get_json().get('isDislike')
    if not isinstance(is_dislike, bool):
        return jsonify(dict(success=False)), 400

    av = fetch_av((id))
    av.is_dislike = is_dislike
    db.session.commit()
    logger.info('Updated dislike of {}'.format(av))
    res = make_response(jsonify(dict(success=True)))
    return handle_response(res)


@app.route('/api/av/<id>/needhd', methods=['PUT'])
def av_need_hd(id):
    """更新is_need_hd, request body中isNeedHd需要为布尔值"""
    is_need_hd = request.get_json().get('isNeedHd')
    if not isinstance(is_need_hd, bool):
        return jsonify(dict(success=False)), 400

    av = fetch_av((id))
    av.is_need_hd = is_need_hd
    db.session.commit()
    logger.info('Updated need_hd of {}'.format(av))
    res = make_response(jsonify(dict(success=True)))
    return handle_response(res)

# 下面是我自己的玩具
# @app.route('/greet/<abbr>')
# def greet(abbr):
#     return get_person_info()
#
#
# @app.route('/person')
# def get_person_info():
#     abbr = request.args.get('abbr')
#     d = {
#         'lxq': {
#             'name': 'luxuanqing',
#             'age': 24
#         },
#         'zhh': {
#             'name': "zhanghuihui",
#             'age': 25
#         }
#     }
#     return jsonify(d[abbr])
