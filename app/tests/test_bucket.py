import os
from unittest import mock

import pytest

from app.bucket import Bucket

REGION = os.environ['REGION']
BUCKET_NAME = os.environ['BUCKET_NAME']


class TestBucket:
    """Tests for operations on AWS S3 bucket."""

    def setup_method(self):
        """Add some photos to the bucket."""

        bucket = Bucket()
  
        with open("app/tests/images/Fujifilm_FinePix_E500.jpg", "rb") as image:
            file = image.read()
            image_bytes = bytearray(file)

        bucket.upload_file(image_bytes, "fuji_test")

        with open("app/tests/images/Pentax_K10D.jpg", "rb") as image:
            file = image.read()
            image_bytes = bytearray(file)

        bucket.upload_file(image_bytes, "pentax_test")
    
    def test_upload_file_ok(self):
        """Test uploading an image to an S3 bucket."""

        bucket = Bucket()
       
        with open("app/tests/images/Nikon_D70.jpg", "rb") as image:
            file = image.read()
            image_bytes = bytearray(file)

        image_name = "nikon_test"

        # Check that image is not currently there
        with pytest.raises(Exception) as e_info:
            bucket.get_file(image_name)
        assert e_info.typename == "NoSuchKey"

        # Upload image
        src = bucket.upload_file(image_bytes, image_name)

        assert src == (
            'https://'
            f'{BUCKET_NAME}.s3.{REGION}'
            f'.amazonaws.com/{image_name}'
        )

        # Check that it's there
        assert bucket.get_file(image_name)

        # Clean up
        bucket.delete_file(image_name)

    def test_upload_bad_credentials(self):
        """Test attempting to upload with bad credentials."""

        bucket = Bucket(aws_access_key="foo", aws_secret_access_key="bar")

        # Upload image
        assert bucket.upload_file(bytearray(), "foo") == None

    def test_get_file(self):
        """Test getting a file."""

        bucket = Bucket()
        assert bucket.get_file("fuji_test")

    def test_delete_file_ok(self):
        """Test deleting a file"""

        bucket = Bucket()

        image_name = "fuji_test"

        # Check that the file is there
        assert bucket.get_file(image_name)

        # Delete it
        bucket.delete_file(image_name)

        # Check that it's not there
        with pytest.raises(Exception) as e_info:
            bucket.get_file(image_name)
        assert e_info.typename == "NoSuchKey"

    def test_delete_file_bad_credentials(self):
        """Test attempting to delete a file with bad credentials."""

        bucket = Bucket(aws_access_key="foo", aws_secret_access_key="bar")

        # Upload image
        assert bucket.delete_file("pentax_test") == None

    def teardown_method(self):
        """Delete remaining images."""

        bucket = Bucket()

        bucket.delete_file("pentax_test")        