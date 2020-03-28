from flask import request, send_file, make_response, jsonify
from jav import app, db
from jav.log import create_logger
from jav.utils import fetch_av, get_imgs_from_av, access_log, update_info

logger = create_logger(__name__)

# views
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
    last_visit = access_log(id, referer=request.headers.get('From-Url'))

    data = request.get_json()
    update_info(av, data)

    return make_response(jsonify({
        'imgs': get_imgs_from_av(av),
        'lastVisit': {
            'timestamp': last_visit.timestamp if last_visit else None,
            'site': last_visit.site if last_visit else None
        },
        'isDislike': av.is_dislike,
        'isNeedHd': av.is_need_hd
    }))


@app.route('/api/javbus/<id>', methods=['POST'])
def javbus(id):
    av = fetch_av(id)
    last_visit = access_log(id, referer=request.headers.get('From-Url'))
    data = request.get_json()
    imgs = data.get('imgs')
    # TODO 错误检验
    # 如果av没有imgs，并且post的data中有imgs，则写入数据库
    if av.imgs_ is None and imgs:
        av.imgs_ = imgs
        db.session.commit()
        logger.info('Updated imgs of {}'.format(av))
    return make_response(jsonify({
        'lastVisit': {
            'timestamp': last_visit.timestamp if last_visit else None,
            'site': last_visit.site if last_visit else None
        },
        'isDislike': av.is_dislike,
        'isNeedHd': av.is_need_hd
    }))


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
    return make_response(jsonify(dict(success=True)))


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
    return make_response(jsonify(dict(success=True)))
