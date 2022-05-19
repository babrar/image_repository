from ..db import db
from .relationship import image_tags


class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    images = db.relationship("Img", secondary=image_tags)
