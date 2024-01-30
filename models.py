from sqlalchemy import Column, String, JSON, DateTime, func
from sqlalchemy.orm import mapped_column
from pgvector.sqlalchemy import Vector

from database import Base, SessionLocal


# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)


class Image(Base):
    """Data model for Image"""

    __tablename__ = "images"

    name = Column(
        String(50),
        primary_key=True)

    aws_image_src = Column(
        String(100),
        nullable=False
    )

    exif_data = Column(
        JSON()
    )

    embedding = mapped_column(Vector(512))

    uploaded_at = Column(
        DateTime,
        nullable=False,
        default=func.now()
    )