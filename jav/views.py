from flask import request, jsonify
from jav import app, db
from jav.log import create_logger
from jav.bots import get_imgs_from_javbus
from jav.models import Av, AccessLog

logger = create_logger(__name__)


def extra_kvs(d: dict, *keys: str) -> dict:
    """尽可能多地根据key筛选出一个字典中所需要的kv，如果字典中没有该key则跳过，如果key对应的val为空也跳过

    Args:
        d: dict 原始的字典
        *keys: str

    Returns:
        dict: 只留下keys中的key的字典
    """
    if not d:
        return {}
    newd = {}
    for key in keys:
        if d.get(key):
            newd.update({key: d[key]})
    return newd


@app.route('/api/av/<id>', methods=['POST', 'PATCH'])
def jav(id):
    """https://github.com/LuXuanqing/indescribable-service/wiki#apiavid"""
    # TODO 检查id类型

    # 解析request body中的json数据
    data = request.json
    logger.debug('data: {}'.format(data))
    # 解析refer，应该是javbus或javlib的url
    refer = request.headers.get('From-Url')
    logger.debug('refer: {}'.format(refer))

    # 先从db中取av，没有则新建
    av = Av.query.get(id)
    if not av:
        logger.debug('{} is not existed'.format(id))
        av = Av(id=id)
        av.save()
        logger.info('Inserted {}.'.format(av))

    # POST method
    if request.method == 'POST':
        # 尝试更新title, casts, genres, imgs, status, rating
        # TODO 前端从javlib获取status和rating
        # 允许初始化赋值的字段
        valid_init_keys = ('title', 'casts', 'genres', 'imgs', 'status', 'rating')
        # 把request body中上述字段非空值的写入
        kvs = extra_kvs(data, *valid_init_keys) if data else {}
        logger.debug('kvs: {}'.format(kvs))
        if kvs:
            av.init_attr(kvs)
            av.save()

        # 如果av没有图片数据，并且请求来自javlib，从javbus爬图片
        if (not av.imgs) and refer and ('javlib' in refer):
            imgs = get_imgs_from_javbus(id)
            if imgs:
                av.init_attr(imgs=imgs).save()
                logger.info('{} update imgs'.format(av))

        # 在插入新的访问记录前，先取好最后一次访问记录
        # TODO 用marshmallow优雅地把Model转成dict
        # TODO 如果为空就不返回该字段
        rtn = {
            'imgs': av.imgs,
            'status': av.status,
            'rating': av.rating,
            'last_visit': av.last_visit
        }

        # 插入新的访问记录
        log = AccessLog(av_id=id, refer=refer)
        log.save()
        logger.info('Inserted {}'.format(log))
        # TODO 尝试去掉jsonify直接返回
        return jsonify(rtn)

    # PATCH method
    elif request.method == 'PATCH':
        # 更新status或rating
        valid_update_keys = ('status', 'rating')
        kvs = extra_kvs(data, *valid_update_keys)
        av.update_attr(**kvs)
        av.save()
        logger.info('update {}: {}'.format(av, kvs))
        return jsonify(kvs)
