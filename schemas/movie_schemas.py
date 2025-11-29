from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class MovieBase(BaseModel):
    title: str
    genre: Optional[str] = None
    description: Optional[str] = None

#добавление фильма
class MovieCreate(MovieBase):
    pass

#обновление инфы про фильм
class MovieUpdate(BaseModel):
    title: Optional[str] = None
    genre: Optional[str] = None
    description: Optional[str] = None
    mood: Optional[str] = None

#возвращает данные пользователю
class Movie(MovieBase):
    model_config = ConfigDict(from_attributes = True)
    id: int
    mood: Optional[str] = None
    created_at: datetime


