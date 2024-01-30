import os

from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.environ.get("SQLALCHEMY_DATABASE_URI")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

with SessionLocal() as session:
    session.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))

Base = declarative_base()