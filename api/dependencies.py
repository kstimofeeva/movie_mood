from database.database import Database
from services.movie_service import MovieService
from services.review_service import ReviewService
from sqlalchemy.orm import Session
from fastapi import Depends
import os

DATABASE_URL = os.getenv("DATABASE_URL")

database = Database(DATABASE_URL)

def get_db() -> Session:
    session = database.get_session()
    try:
        yield session
    finally:
        session.close()

def get_movie_service(db: Session = Depends(get_db)) -> MovieService:
    return MovieService(db)

def get_review_service(db: Session = Depends(get_db)) ->ReviewService:
    return ReviewService(db)