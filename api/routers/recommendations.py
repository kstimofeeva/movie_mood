from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from services.movie_service import MovieService
from schemas.movie_schemas import Movie
from api.dependencies import get_movie_service

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.get("/by-mood/", response_model=List[Movie])
def get_recommendations_by_mood(
        mood: str = Query(..., description="Настроение для рекомендаций"),
        limit: int = Query(10, ge=1, le=50, description="Количество рекомендаций"),
        movie_service: MovieService = Depends(get_movie_service)
):
    try:
        valid_moods = ['neutral', 'positive', 'negative']
        if mood.lower() not in valid_moods:
            raise HTTPException(status_code=400, detail="недопустимое настроение")

        movies = movie_service.get_movies_by_mood(mood.lower())
        if not movies:
            raise HTTPException(status_code=404, detail="aильмы с таким настроением не найдены")
        return movies[:limit]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ошибка при получении фильмов")


