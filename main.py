from typing import Annotated

from fastapi import (
    FastAPI, 
    Depends, 
    HTTPException, 
    Query, 
    Body,
    Header,
    UploadFile,  
    status
)
from sqlalchemy.orm import Session

import crud
import models
import schemas
import image_utils
import bucket
import clip
import auth
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/images/", response_model=list[schemas.Image])
def get_images(
    q: Annotated[str | None, Query(max_length=100)] = None,
    limit: int = 50,
    db: Session = Depends(get_db)):

    return crud.get_images(limit=limit, search_term=q, db=db)

@app.post("/images/", response_model=schemas.Image, status_code=201)
def upload_image(
    file: UploadFile, 
    image_name: Annotated[str, Body()],
    hashed_pw: Annotated[str, Header(alias="HTTPBearer")], 
    db: Session = Depends(get_db)):

    if not auth.verify_admin(hashed_pw):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )
    
    if crud.get_image(image_name=image_name, db=db):
        raise HTTPException(status_code=400, detail="File name already taken")
    
    exif_data = image_utils.scrape_exif(file.file)
    file.file.seek(0)

    aws_image_src = bucket.upload_file(file.file, image_name)
    image_embedding = clip.get_image_embedding(aws_image_src)

    image = schemas.ImageCreate(
        name=image_name,
        aws_image_src=aws_image_src,
        exif_data=exif_data,
        embedding=image_embedding
    )

    image = crud.create_image(image=image, db=db)

    return image

@app.delete("/images/{image_name}")
def delete_image(
    image_name: str, 
    hashed_pw: Annotated[str, Header(alias="HTTPBearer")],
    db: Session = Depends(get_db)):
    
    if not auth.verify_admin(hashed_pw):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )
    
    if not crud.get_image(image_name=image_name, db=db):
        raise HTTPException(status_code=404, detail="File not found")
    
    crud.delete_image(image_name=image_name, db=db)
    bucket.delete_file(image_name)

    return {"Message": "Successfully deleted file."}
