from jav import db
from jav.models import Av, History
from jav import bots
from jav.log import create_logger

logger = create_logger(__name__)

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


def access_log(id, referer):
    """
    获取上次访问信息，并添加这次访问信息
    :param id:
    :return: 上次访问信息<History>
    """
    last_visit = History.query.filter_by(av_id=id).order_by(History.timestamp.desc()).first()
    # 记录这次访问
    # TODO 写入访问历史（最好可以通过fetch_av来创建）
    # TODO 用装饰器做成每次请求后自动添加访问记录
    this_visit = History(av_id=id, site=referer)
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