from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from numpy.typing import NDArray

import crud, models, schemas
from database import SessionLocal, engine
from clip import get_text_encoding

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/images/", response_model=list[schemas.Image])
def read_items(
    q: Annotated[str | None, Query(max_length=100)] = None,
    limit: int = 50,
    db: Session = Depends(get_db)):

    text_embedding = get_text_encoding(q)

    items = crud.get_images(db, limit=limit, text_embedding=text_embedding)
    return items

# TODO: POST /images/ with S3 upload logic, check for whether image name exists.