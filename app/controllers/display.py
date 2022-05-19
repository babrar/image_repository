from ..db import db
from ..models.image import Img
from ..models.tag import Tag
from .utils import hamming_distance
from .utils import image_hash

# distances lesser than threshold indicates similarity between two images
SIMILARITY_DISTANCE_THRESHOLD = 25


def get_images_from_tag(tag):
    """Return images that have the given tag.
    Param:
        tag - str - tag to search images by
    Return:
        list[Img] - images that match the tag
    """
    tag = tag.lower()
    t = Tag.query.filter_by(name=tag).first()
    if t is None:
        return []
    con = db.engine.connect()
    query = f"""
    SELECT
        images.img  AS pic,
        images.name AS image_name,
        tags.name AS tag_name,
        image_tags.image_id
    FROM tags
    INNER JOIN image_tags ON tags.id = image_tags.tag_id
    INNER JOIN images ON image_tags.image_id = images.id
    WHERE tag_name = "{tag}"
    """
    resp = con.execute(query).fetchall()
    image_list = []
    for row in resp:
        image_list.append(row[0])
    return image_list


def get_similar_images(image):
    given_img_hash = image_hash(image.read())
    all_imgs = Img.query.all()
    result = []
    for img in all_imgs:
        if (
            hamming_distance(img.img_hash, given_img_hash)
            < SIMILARITY_DISTANCE_THRESHOLD
        ):
            result.append(img.img)
    return result
