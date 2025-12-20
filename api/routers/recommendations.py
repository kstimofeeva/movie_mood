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
    movies = movie_service.get_movies_by_mood(mood)
    if not movies:
        raise HTTPException(status_code=404, detail="ильмы с таким настроением не найдены")
    return movies


