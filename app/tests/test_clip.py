from numpy.linalg import norm
from numpy import isclose

from app.bucket import Bucket
from app.clip import EMBEDDING_SIZE, get_image_embedding, get_text_embedding


def test_get_text_embedding():
    """Test getting text embedding from CLIP."""

    embedding = get_text_embedding("this is some input text")

    assert isinstance(embedding, list)
    assert (len(embedding) == EMBEDDING_SIZE)
    assert (isclose(norm(embedding), 1))

def test_get_image_embedding():
    """Test getting an image embedding from CLIP."""

    bucket = Bucket()

    with open("app/tests/images/Fujifilm_FinePix_E500.jpg", "rb") as image:
        file = image.read()
        image_bytes = bytearray(file)

    src = bucket.upload_file(image_bytes, "fuji_test")

    embedding = get_image_embedding(src)

    assert isinstance(embedding, list)
    assert (len(embedding) == EMBEDDING_SIZE)
    assert (isclose(norm(embedding), 1))

    bucket.delete_file("fuji_test")

