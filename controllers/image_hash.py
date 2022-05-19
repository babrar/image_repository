import io
from PIL import Image
import imagehash

def image_hash(image):
    img = Image.open(io.BytesIO(image))
    return imagehash.whash(img)