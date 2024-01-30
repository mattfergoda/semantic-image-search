from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
from models import Image


def get_image(db: Session, image_name: str):
    return (
        db.query(Image)
        .filter(Image.image_name == image_name)
        .first()
    )

def get_images(db: Session, limit: int = 50, text_embedding = None):
    if text_embedding:
        return (
            db.scalars(select(Image)
                .order_by(Image.embedding.max_inner_product(text_embedding))
                .limit(5))
        )
    return db.query(Image).limit(limit).all()

def create_image(db: Session, image: schemas.ImageCreate):
    db_image = Image(**image.model_dump())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image