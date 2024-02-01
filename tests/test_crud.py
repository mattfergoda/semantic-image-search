import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import numpy as np

from database import Base
from models import Image
from clip import EMBEDDING_SIZE
import schemas
import crud

SQLALCHEMY_TEST_DATABASE_URL = "postgresql:///semantic_pic_test"

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)


class TestCRUD:
    """Tests for CRUD database operations."""

    @pytest.fixture
    def session(self):
        Base.metadata.create_all(bind=engine)
        session = TestingSessionLocal()

        self.image_1 = Image(
            name="test1", 
            aws_image_src="https://test1.jpg", 
            exif_data={"field1" : "value1"},
            embedding = np.random.random(EMBEDDING_SIZE).tolist()
        )
        self.image_2 = Image(
            name="test2", 
            aws_image_src="https://test2.jpg", 
            exif_data={"field1" : "value1"},
            embedding = np.random.random(EMBEDDING_SIZE).tolist()
        )
        self.images = [self.image_1, self.image_2]
        session.bulk_save_objects(self.images)
        session.commit()

        yield session

        session.close()
        Base.metadata.drop_all(bind=engine)

    def test_get_image(self, session: Session):
        """Test getting a single image."""
        
        image = crud.get_image(session, "test1")
        assert image.name == "test1"
        assert image.aws_image_src == "https://test1.jpg"
        assert image.exif_data == {"field1" : "value1"}
        assert isinstance(image.embedding, np.ndarray)
        assert len(image.embedding) == EMBEDDING_SIZE

    def test_get_images_with_search(self, session: Session):
        """Test getting multiple images with a search term."""

        image_names = [i.name for i in self.images]
        images = crud.get_images(session, search_term="foo")

        for image in images:
            assert image.name in image_names
            assert isinstance(image.aws_image_src, str)
            assert isinstance(image.exif_data, dict)
            assert isinstance(image.embedding, np.ndarray)

    def test_get_images_no_search(self, session: Session):
        """Test getting multiple images without a search term."""

        image_names = [i.name for i in self.images]
        images = crud.get_images(session)

        for image in images:
            assert image.name in image_names
            assert isinstance(image.aws_image_src, str)
            assert isinstance(image.exif_data, dict)
            assert isinstance(image.embedding, np.ndarray)

    def test_create_image(self, session: Session):
        """Test creating an image."""

        image = schemas.ImageCreate(
            name="image3",
            aws_image_src="https://test3.jpg",
            exif_data={"field1" : "value1"},
            embedding=np.random.random(EMBEDDING_SIZE).tolist()
        )
        crud.create_image(session, image)

        db_image = crud.get_image(session, image.name)

        assert db_image.name == image.name
        assert db_image.aws_image_src == image.aws_image_src
        assert db_image.exif_data == image.exif_data
        assert isinstance(db_image.embedding, np.ndarray)
        assert len(db_image.embedding) == EMBEDDING_SIZE

    def test_delete_image(self, session: Session):
        """Test deleting an image."""

        image_name = self.image_1.name
        image_1 = crud.get_image(session, image_name)

        assert image_1 is not None

        crud.delete_image(session, image_name)
        image_none = crud.get_image(session, image_name)

        assert image_none is None

        

