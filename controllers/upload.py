import re
from werkzeug.utils import secure_filename
from db import db
from models.image import Img, Tag
import io
from PIL import Image
import imagehash


def image_hash(image):
    img = Image.open(io.BytesIO(image))
    img_hash = imagehash.whash(img)
    # convert from hex string to int
    return int(str(img_hash), 16)


def tokenize(s):
    """Remove punctuations and tokenize the given string into words
    Param:
        s - str - string to tokenize
    Return:
        list[str] - tokenized list of words
    """
    # transform _ and - to whitespace since they usually delimit two separate words
    res = s.replace("-", " ").replace("_", " ")
    # remove any punctuation marks
    res = re.sub("[^\w\s]", "", res)
    return res.split(" ")


def upload_images(pic, tags):
    """Upload image and tags to database
    param:
        pic - IO like object that can be read - picture to be uploaded
        tags - list[str] - tags associcated with picture
    return:
        bool - True on success
    """

    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    if not filename or not mimetype or "image" not in str(mimetype):
        return False

    # SQLAlchemy raises exception on failure
    try:
        img_payload = pic.read()
        img = Img(
            img=img_payload,
            name=filename,
            mimetype=mimetype,
            img_hash=image_hash(img_payload),
        )

        # remove extension from file name
        filename, ext = filename.split(".")
        # tokenize the filename into separate words
        # and use the tokens as additional tags
        tags_from_filename = tokenize(filename)

        _upload_tags(img, tags.split(",") + tags_from_filename + [ext])
        db.session.add(img)
        db.session.commit()

    except Exception as e:
        print(e.with_traceback())
        return False

    return True


def _upload_tags(image, tags):
    """Upload tags for corresponding image.
    Param:
        image - db.Model - image object from the database
        tags - list[str] - tags to upload
    Return:
        raise exception on failure
    """
    # remove empty strings from tag list
    tags = [t for t in tags if t]
    for tag in tags:
        # if tag already exists, simply update the relationship table
        t = db.session.query(Tag).filter_by(name=tag).first()
        if t is not None:
            t.images.append(image)
            db.session.add(t)
        # if tag doesn't exist, then create it in tags table
        else:
            t = Tag(name=tag)
            t.images.append(image)
            db.session.add(t)
    db.session.commit()
