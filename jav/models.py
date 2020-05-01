from jav import db
from datetime import datetime
from enum import Enum, auto
from jav.log import create_logger

logger = create_logger(__name__)


class BaseMixin(object):
    """https://stackoverflow.com/questions/35814211/how-to-add-a-custom-function-method-in-sqlalchemy-model-to-do
    -crud-operations"""

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            logger.error(e)
            db.session.rollback()
            raise Exception('failed to save {}'.format(self))
        finally:
            return self


class Status(Enum):
    """WANTED > DOWNLOADING > WATCHED > OWNED
    """
    WANTED = auto()
    DOWNLOADING = auto()
    WATCHED = auto()
    OWNED = auto()


class Rating(Enum):
    """DISLIKED > NETURAL > FAVORITE"""
    DISLIKED = auto()
    NETURAL = auto()
    FAVORITE = auto()


class Av(BaseMixin, db.Model):
    """新建时必须穿入id"""
    id = db.Column(db.String, primary_key=True, index=True)
    title = db.Column(db.String)
    casts = db.Column(db.JSON)
    genres = db.Column(db.JSON)
    imgs = db.Column(db.JSON)
    status = db.Column(db.Enum(Status))
    rating = db.Column(db.Enum(Rating))
    logs = db.relationship('AccessLog', order_by="desc(AccessLog.ts)", lazy='dynamic')

    def __repr__(self):
        return '<Av {}>'.format(self.id)

    @property
    def last_visit(self):
        # 获取最后一条访问记录, <AccessLog>
        last_log = self.logs.limit(1).first()
        # 如果没有last log，则返回None
        if not last_log:
            return None
        return {
            'refer_site': last_log.refer_site,
            'ts': last_log.ts
        }

    def init_attr(self, **kw):
        """初始化自己的属性，不允许修改已赋值的属性
        Args:
            **kw:
        """
        for key, value in kw.items():
            logger.debug('{}: {}'.format(key, value))
            # 检查该字段是否已有值，是则跳过
            if getattr(self, key):
                logger.warning('{} has value: {}, skip init_attr'.format(key, getattr(self, key)))
                continue
            # 初始化赋值
            setattr(self, key, value)
            logger.info('Av attribute modified {}: {}'.format(key, value))
        return self

    def update_attr(self, **kw):
        """更新自己的属性，不允许写入空值

        Args:
            **kw:
        """
        for key, value in kw.items():
            logger.debug('{}: {}'.format(key, value))
            # 检查更新的指是否为空，如果是则跳过更新该字段
            if not value:
                logger.warning('{} is empty, skip update_attr'.format(key))
                continue
            # 更新属性
            setattr(self, key, value)
            logger.info('Av attribute modified {}: {}'.format(key, value))
        return self


class AccessLog(BaseMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    av_id = db.Column(db.Integer, db.ForeignKey('av.id'), index=True)
    refer = db.Column(db.String)
    ts = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def refer_site(self):
        if not self.refer:
            return ''
        elif 'javbus' in self.refer:
            return 'javbus'
        elif 'javlib' in self.refer:
            return 'javlib'
        else:
            return 'other'

    def __repr__(self):
        return '<AccessLog {} @ {} from {}>'.format(self.av_id, self.ts, self.refer_site)