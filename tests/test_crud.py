import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import numpy as np
from pgvector.sqlalchemy import Vector

from database import Base
from models import Image, EMBEDDING_SIZE, Vector
import crud

SQLALCHEMY_TEST_DATABASE_URL = "postgresql:///semantic_pic_test"

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

@pytest.fixture
def session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()

    images = [
        Image(
        name="test1", 
        aws_image_src="https://test1.jpg", 
        exif_data={"field1" : "value1"},
        embedding = np.random.random(EMBEDDING_SIZE).tolist()),
        Image(
        name="test2", 
        aws_image_src="https://test2.jpg", 
        exif_data={"field1" : "value1"},
        embedding = np.random.random(EMBEDDING_SIZE).tolist())
    ]
    session.bulk_save_objects(images)
    session.commit()

    yield session

    session.close()
    Base.metadata.drop_all(bind=engine)

def test_get_image(session: Session):
    """Test getting a single image."""
    
    image = crud.get_image(session, "test1")
    assert image.name == "test1"
    assert image.aws_image_src == "https://test1.jpg"
    assert image.exif_data == {"field1" : "value1"}
    assert isinstance(image.embedding, np.ndarray)
    assert len(image.embedding) == EMBEDDING_SIZE