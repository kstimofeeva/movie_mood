from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime

class Base(DeclarativeBase): pass

class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key = True, index = True)
    title = Column(String(255), nullable=False, index = True)
    genre = Column(String(100))
    description = Column(Text)
    mood = Column(String(50))
    created_at = Column(DateTime, default = datetime.utcnow)

    reviews = relationship('Review', back_populates = 'movie', cascade='all, delete-orphan')

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key = True, index = True)
    movie_id = Column(Integer, ForeignKey('movies.id', ondelete = 'CASCADE'))
    review_text = Column(Text)
    sentiment = Column(String(20))
    sentiment_score = Column(Float)
    created_at = Column(DateTime, default = datetime.utcnow)

    movie = relationship('Movie', back_populates = 'reviews')

