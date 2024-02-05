import os
from dateutil import parser

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app, get_db
from app.database import Base


ADMIN_PW = os.environ["ADMIN_PW"]
REGION = os.environ['REGION']
BUCKET_NAME = os.environ['BUCKET_NAME']
SQLALCHEMY_TEST_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']

TEST_IMAGES = {
    "pentax_test": "Pentax_K10D.jpg",
    "nikon_test": "Nikon_D70.jpg"
}

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URI)

TestingSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def setup():
    """Add some test images."""

    Base.metadata.create_all(bind=engine)

    for name, fname in TEST_IMAGES.items():
        with open(f"app/tests/images/{fname}", "rb") as image:
            file = image.read()
        
        client.post(
            "/images/",
            headers={"HTTPBearer": ADMIN_PW},
            data={"image_name": name},
            files={
                "file": (fname, file)
            }
        )

def test_get_image_okay():
    """Test getting an image"""

    image_name = "nikon_test"
    response = client.get(f"/images/{image_name}")

    data = response.json()
    
    assert response.status_code == 200
    assert data["name"] == image_name
    assert data["aws_image_src"] == (
        f'https://{BUCKET_NAME}.s3.{REGION}.amazonaws.com/{image_name}'
    )
    assert data["exif_data"] == {
        'ResolutionUnit': 2, 
        'ExifOffset': 198, 
        'Make': 'NIKON CORPORATION', 
        'Model': 'NIKON D70', 
        'Software': 'GIMP 2.4.5', 
        'Orientation': 1, 'DateTime': 
        '2008:07:31 10:03:44', 
        'XResolution': 240.0, 
        'YResolution': 240.0
    } 

    assert _is_valid_datetime_string(data["uploaded_at"])

def test_get_image_not_found():
    """Test getting an image that doesn't exist"""

    image_name = "foo"
    response = client.get(f"/images/{image_name}")

    data = response.json()
    
    assert response.status_code == 404
    assert data == {"detail": "File not found"}

def test_get_images_no_search():
    """Test getting images without a search term"""

    response = client.get(f"/images/")
    data = response.json()

    assert len(data) == 2
    
    for image in data:
        assert image["name"] in TEST_IMAGES.keys()
        assert isinstance(image["aws_image_src"], str)
        assert isinstance(image["exif_data"], dict)
        assert isinstance(image["uploaded_at"], str)
        assert _is_valid_datetime_string(image["uploaded_at"])

def test_get_images_with_search():
    """Test getting images with a search term"""

    response = client.get(
        f"/images/", 
        params={
            "q": "a lizard on a leaf"
        }
    )
    data = response.json()

    assert len(data) == 2
    
    for image in data:
        assert image["name"] in TEST_IMAGES.keys()
        assert isinstance(image["aws_image_src"], str)
        assert isinstance(image["exif_data"], dict)
        assert isinstance(image["uploaded_at"], str)
        assert _is_valid_datetime_string(image["uploaded_at"])
    
    assert data[0]["name"] == "nikon_test"
    assert data[1]["name"] == "pentax_test"

def test_get_images_with_different_search():
    """Test getting images with a different search term"""

    response = client.get(
        f"/images/", 
        params={
            "q": "a rose"
        }
    )
    data = response.json()

    assert len(data) == 2
    
    for image in data:
        assert image["name"] in TEST_IMAGES.keys()
        assert isinstance(image["aws_image_src"], str)
        assert isinstance(image["exif_data"], dict)
        assert isinstance(image["uploaded_at"], str)
        assert _is_valid_datetime_string(image["uploaded_at"])
    
    assert data[0]["name"] == "pentax_test"
    assert data[1]["name"] == "nikon_test"

def test_post_image_okay():
    """Test adding an image."""

    image_name = "fuji_test"
    image_fname = "Fujifilm_FinePix_E500.jpg"

    # Make sure it's not there to start with
    response = client.get(f"/images/{image_name}")
    data = response.json()
    assert response.status_code == 404
    assert data == {"detail": "File not found"}

    with open(f"app/tests/images/{image_fname}", "rb") as image:
        file = image.read()

    response = client.post(
        "/images/",
        headers={"HTTPBearer": ADMIN_PW},
        data={"image_name": image_name},
        files={
            "file": (image_fname, file)
        }
    )
    
    data = response.json()
  
    assert response.status_code == 201
    assert data["name"] == image_name
    assert data["aws_image_src"] == (
        f'https://{BUCKET_NAME}.s3.{REGION}.amazonaws.com/{image_name}'
    )
    assert data["exif_data"] == {
            'ResolutionUnit': 2,
            'ExifOffset': 266, 
            'Make': 'FUJIFILM', 
            'Model': 'FinePix E500   ', 
            'Software': 'GIMP 2.4.5', 
            'Orientation': 1, 
            'DateTime': '2008:07:31 16:49:10', 
            'YCbCrPositioning': 2, 
            'Copyright': '    ', 
            'XResolution': 96.0, 
            'YResolution': 96.0
    }

    assert _is_valid_datetime_string(data["uploaded_at"])

    client.delete(
        f"/images/{image_name}",
        headers={"HTTPBearer": ADMIN_PW}
    )

def test_post_dupe_image():
    """Test adding an image with an existing file name."""

    image_name = "nikon_test"
    image_fname = "Nikon_D70.jpg"

    with open(f"app/tests/images/{image_fname}", "rb") as image:
        file = image.read()

    response = client.post(
        "/images/",
        headers={"HTTPBearer": ADMIN_PW},
        data={"image_name": image_name},
        files={
            "file": (image_fname, file)
        }
    )
    
    data = response.json()
    print(data)
    assert response.status_code == 400
    assert data == {"detail": "File name already taken"}

def test_post_image_unauth():
    """Test adding an image with incorrect token."""

    image_name = "fuji_test"
    image_fname = "Fujifilm_FinePix_E500.jpg"

    with open(f"app/tests/images/{image_fname}", "rb") as image:
        file = image.read()

    response = client.post(
        "/images/",
        headers={"HTTPBearer": "foo"},
        data={"image_name": image_name},
        files={
            "file": (image_fname, file)
        }
    )
    
    data = response.json()
    print(data)
    assert response.status_code == 401
    assert data == {"detail": "Unauthorized"}

def test_delete_image_okay():
    """Test deleting an image"""

    image_name = "nikon_test"

    # Make sure the image is there already.
    response = client.get(f"/images/{image_name}")

    data = response.json()
    
    assert response.status_code == 200
    assert data["name"] == image_name

    response = client.delete(
        f"/images/{image_name}",
        headers={"HTTPBearer": ADMIN_PW},
    )
    data = response.json()

    assert response.status_code == 200
    assert data == {'Message': 'Successfully deleted file.'}

    # Add the image back
    image_fname = TEST_IMAGES[image_name]

    with open(f"app/tests/images/{image_fname}", "rb") as image:
        file = image.read()

    client.post(
        "/images/",
        headers={"HTTPBearer": ADMIN_PW},
        data={"image_name": image_name},
        files={
            "file": (image_fname, file)
        }
    )

def test_delete_image_not_found():
    """Test deleting an image that doesn't exist"""

    image_name = "foo"
    
    response = client.delete(
        f"/images/{image_name}",
        headers={"HTTPBearer": ADMIN_PW},
    )
    data = response.json()

    assert response.status_code == 404
    assert data == {"detail": "File not found"}

def test_delete_image_unauth():
    """Test deleting an image with the incorrect token"""

    image_name = "nikon_test"

    # Make sure the image is there already.
    response = client.get(f"/images/{image_name}")

    data = response.json()
    
    assert response.status_code == 200
    assert data["name"] == image_name

    response = client.delete(
        f"/images/{image_name}",
        headers={"HTTPBearer": "foo"},
    )
    data = response.json()

    assert response.status_code == 401
    assert data == {"detail": "Unauthorized"}

def teardown():
    for name, fname in TEST_IMAGES.items():
        
        client.delete(
            f"/images/{name}",
            headers={"HTTPBearer": ADMIN_PW}
        )

    Base.metadata.drop_all(bind=engine)

def _is_valid_datetime_string(date_string):
    try:
        # Attempt to parse the string into a datetime object
        parsed_datetime = parser.parse(date_string)
        return True
    except ValueError:
        # If parsing fails, it's not a valid datetime string
        return False