from datetime import datetime

from pydantic import BaseModel


class ImageBase(BaseModel):
    name: str


class ImageCreate(ImageBase):
    aws_image_src : str
    exif_data: object
    embedding: list


class Image(ImageBase):
    aws_image_src : str
    exif_data: object
    uploaded_at : datetime

    class Config:
        orm_mode = True