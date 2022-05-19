from operator import index
from flask import Flask, request, render_template, redirect, flash, session
from db import db_init, db
from models.image import Img, Tag
from controllers.upload import upload_images
import base64

app = Flask(__name__)
app.secret_key = "abc"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///image.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db_init(app)


@app.route("/")
def redir():
    return redirect("/home")


@app.route("/home")
def index():
    # session.pop('_flashes', None)
    return render_template("index.html")


@app.route("/search")
def search():
    return render_template("search.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return render_template("upload.html")

    pic = request.files.get("pic")
    tags = request.form.get("inputTags")

    # let controller handle upload
    if (upload_images(pic, tags)):
        flash("Image and tag(s) uploaded")
    else:
        flash("Unable to upload image and tags")

    # session.pop('_flashes', None)

    return render_template("upload.html")


@app.route("/tag")
def tag():
    return render_template("tag.html")


@app.route("/similar")
def similar():
    return "Developing"


@app.route("/display_tag_matches", methods=["POST"])
def display_tag_matches():
    pic_list = None
    return render_template("display.html", pic_list=pic_list)


@app.route("/display_similar", methods=["POST"])
def display_similar():
    return "Developing"
