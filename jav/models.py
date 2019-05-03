from jav import db
from datetime import datetime
import json


class Av(db.Model):
    id = db.Column(db.String(16), primary_key=True, index=True)
    genres = db.Column(db.String)
    casts = db.Column(db.String)
    imgs = db.Column(db.Text)
    is_dislike = db.Column(db.Boolean, default=False)
    is_need_hd = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Av {}>'.format(self.id)

    # TODO 监听commit等事件，用字段原名自动实现以下装饰器
    @property
    def genres_(self):
        return json.loads(self.genres) if isinstance(self.genres, str) else None

    @genres_.setter
    def genres_(self, value):
        if not isinstance(value, list):
            raise TypeError('new value must be a list of str')
        self.genres = json.dumps(value)

    @property
    def casts_(self):
        return json.loads(self.casts) if isinstance(self.casts, str) else None

    @casts_.setter
    def casts_(self, value):
        if not isinstance(value, list):
            raise TypeError('new value must be a list of str')
        self.casts = json.dumps(value)

    @property
    def imgs_(self):
        return json.loads(self.imgs) if isinstance(self.imgs, str) else None

    @imgs_.setter
    def imgs_(self, value):
        if not isinstance(value, list):
            raise TypeError('new value must be a list of str')
        self.imgs = json.dumps(value)


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    av_id = db.Column(db.Integer, db.ForeignKey('av.id'), index=True)
    site = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<History {}@{}>'.format(self.av_id, self.timestamp)
