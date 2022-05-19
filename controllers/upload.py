from werkzeug.utils import secure_filename
from db import db
from models.image import Img
from models.tag import Tag
from .utils import image_hash, tokenize, remove_empty_tags


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
    tags = remove_empty_tags(tags)
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
