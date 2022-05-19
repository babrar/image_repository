from ..db import db


class Img(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    img = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    img_hash = db.Column(db.Integer, nullable=False)
