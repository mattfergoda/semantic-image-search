from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
import clip
from models import Image


def get_image(db: Session, image_name: str):
    """Get one image based on its name"""

    return (
        db.query(Image)
        .filter(Image.name == image_name)
        .first()
    )

def get_images(db: Session, limit: int = 50, search_term = None):
    """
    Get multiple images
    limit: Number of images to limit results to
    search_term: string by which to do a semantic search
    """

    embedding = clip.get_text_embedding(search_term) if search_term else None

    if embedding:
        return (
            db.scalars(select(Image)
                .order_by(Image.embedding.max_inner_product(embedding))
                .limit(limit))
        )
    return (
            db.scalars(select(Image)
                .order_by(Image.uploaded_at.desc())
                .limit(limit))
        )

def create_image(db: Session, image: schemas.ImageCreate):
    """Create a new image"""

    db_image = Image(**image.model_dump())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

def delete_image(db: Session, image_name: str):
    """Delete an image."""

    db_image = db.query(Image).filter(Image.name == image_name).first()
    db.delete(db_image)
    db.commit()
    return db_image