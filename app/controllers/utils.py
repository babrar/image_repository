import io
from PIL import Image
import imagehash
import re


def image_hash(image):
    """Perform wavelet hashing of given image. Two similar images
    should produce similar hashes.
    Note:
    The output hash is a 64 bit unsigned integer.
    SQLite can only store upto 64 bit signed integers.

    Hacky solution: Truncate the hash to 63 bits.
    """
    img = Image.open(io.BytesIO(image))
    img_hash = imagehash.whash(img)

    # truncate to 63 bits for SQLite compliance
    truncated_hash = 0x7FFFFFFFFFFFFFFF & int(str(img_hash), 16)

    # convert from hex to int
    return truncated_hash


def tokenize(s):
    """Remove punctuations and tokenize the given string into words
    Param:
        s - str - string to tokenize
    Return:
        list[str] - tokenized list of words
    """
    # transform _ and - to whitespace
    # since they usually delimit two separate words
    res = s.replace("-", " ").replace("_", " ")
    # remove any punctuation marks
    res = re.sub("[^\w\s]", "", res)
    return res.split(" ")


def remove_empty_tags(tag_list):
    return [t for t in tag_list if t]


def hamming_distance(x, y):
    """Hamming distance alg to determine similarity between two hashes
    :type x: int
    :type y: int
    :rtype: int
    """
    ans = 0
    for i in range(63, -1, -1):
        b1 = x >> i & 1
        b2 = y >> i & 1
        ans += not (b1 == b2)
    return ans
