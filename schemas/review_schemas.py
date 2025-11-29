from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class ReviewBase(BaseModel):
    review_text: str

class ReviewCreate(ReviewBase):
    movie_id: int

class Review(ReviewBase):
    model_config = ConfigDict(from_attributes = True)
    id: int
    movie_id : int
    sentiment: Optional[str] = None
    sentiment_score: Optional[float] = None
    created_at: datetime
