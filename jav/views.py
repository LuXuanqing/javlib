from flask import request, send_file, make_response, jsonify
from jav import app, db
from jav.models import Av, History
from jav import bots
from jav.log import create_logger

logger = create_logger(__name__)


@app.route('/content')
def content():
    res = make_response(send_file('templates/content.html'))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


@app.route('/api/av/<id>', methods=['POST'])
def check_av(id, genres=None, casts=None):
    """
    更新genres, casts，并获取imgs, 上次访问

    :param id: av的番号，例如SSNI-413
    :param genres: 类别，默认不穿，自动从request中解析
    :param casts: 演员，默认不穿，自动从request中解析
    :return:
    """
    av = fetch_av(id)
    last_visit = History.query.filter_by(av_id=id).order_by(History.timestamp.desc()).first()
    # 记录这次访问
    # TODO 用装饰器做成每次请求后自动添加访问记录
    this_visit = History(av_id=id, site=request.referrer)
    db.session.add(this_visit)
    db.session.commit()
    logger.info('Insert {}'.format(this_visit))

    # 如果本来没有genres, casts，则更新该字段
    data = request.get_json()
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

    res = make_response(jsonify({
        'imgs': get_imgs_from_av(av),
        'lastVisit': {
            'timestamp': last_visit.timestamp if last_visit else None,
            'site': last_visit.site if last_visit else None
        },
        'isDislike': av.is_dislike,
        'isNeedHd': av.is_need_hd
    }))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


def fetch_av(id):
    # 从数据库查询，没有则新建
    av = Av.query.get(id)
    if not av:
        av = Av(id=id)
        db.session.add(av)
        db.session.commit()
        logger.info('Inserted {}.'.format(av))
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


@app.route('/api/av/<id>/imgs', methods=['GET', 'POST'])
def handle_av_imgs(id):
    av = fetch_av(id)
    if request.method == 'GET':
        # TODO 如果返回数据为空，应该不是200
        return jsonify(get_imgs_from_av(av))

    if request.method == 'POST':
        # TODO 错误检验
        # TODO 写入访问历史（最好可以通过fetch_av来创建）
        # 如果av没有imgs，并且post的data中有imgs，则写入数据库
        av.imgs_ = request.get_json()
        db.session.commit()
        logger.info('Updated imgs of {}'.format(av))
        return 'ok'


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
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


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
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res
