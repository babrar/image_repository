from enum import unique
from db import db

image_tags = db.Table(
    "image_tags",
    db.Column("image_id", db.ForeignKey("images.id")),
    db.Column("tag_id", db.ForeignKey("tags.id")),
)


class Img(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    img = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    img_hash = db.Column(db.Integer, nullable=False)


class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    images = db.relationship("Img", secondary=image_tags)
