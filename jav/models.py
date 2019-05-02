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

    def to_json(self):
        # TODO implement this methods
        pass

    def from_json(self):
        # TODO implement this methods
        pass


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    av_id = db.Column(db.Integer, db.ForeignKey('av.id'), index=True)
    site = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<History {}@{}>'.format(self.av_id, self.timestamp)

