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

    @property
    def genres_(self):
        return json.loads(self.genres)


    def __repr__(self):
        return '<Av {}>'.format(self.id)

    def to_json(self):
        """把imgs, genres, casts从Str转换成Json"""

        # TODO 换一个更优雅的方法实现
        if type(self.genres) == str:
            self.genres = json.loads(self.genres)
        if type(self.casts) == str:
            self.casts = json.loads(self.casts)
        if type(self.imgs) == str:
            self.imgs = json.loads(self.imgs)

        return self

    def to_str(self):
        """把imgs, genres, casts从list对象转换成str用于写入数据库"""

        # TODO 换一个更优雅的方法实现
        if type(self.genres) == list:
            self.genres = json.dumps(self.genres)
        if type(self.casts) == list:
            self.casts = json.dumps(self.casts)
        if type(self.imgs) == list:
            self.imgs = json.dumps(self.imgs)

        return self
    # TODO 监听commit等事件，自动实现这两个方法

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    av_id = db.Column(db.Integer, db.ForeignKey('av.id'), index=True)
    site = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<History {}@{}>'.format(self.av_id, self.timestamp)

