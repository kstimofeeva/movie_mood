from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from services.movie_service import MovieService
from schemas.movie_schemas import MovieCreate, MovieUpdate, Movie
from api.dependencies import get_movie_service

router = APIRouter(prefix="/movies", tags=["movies"])

@router.post("/", response_model=Movie, status_code=201)
def create_movie(
        movie: MovieCreate,
        movie_service: MovieService = Depends(get_movie_service)
):
    try:
        return movie_service.create_movie(movie)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model = List[Movie])
def get_movies(
        skip: int = Query(0, ge=0, description= "Пропустить первые  записей"),
        limit:int = Query(100, ge=1, le=100, descriptoin="Лимит записей"),
        movie_service: MovieService = Depends(get_movie_service)
):
    return movie_service.get_all_movies(skip=skip, limit=limit)

@router.get("/{movie_id}", response_model=Movie)
def get_movie(movie_id:int, movie_service: MovieService = Depends(get_movie_service)):
    movie = movie_service.get_movie(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    return movie

@router.get("/search/", response_model=List[Movie])
def search_movies(
        title: Optional[str] = Query(None, description="Поиск по названию"),
        genre: Optional[str] = Query(None, description="Поиск по жанру"),
        mood: Optional[str] = Query(None, description="Поиск по настроению"),
        movie_service: MovieService = Depends(get_movie_service)
):
    movies = movie_service.get_all_movies()
    result = []
    for movie in movies:
        if title and title.lower() not in movie.title.lower():
            continue
        if genre and genre.lower not in (movie.genre or "").lower():
            continue
        if mood and mood.lower not in (movie.mood or "").lower():
            continue
        result.append(movie)
    return result

@router.patch("/{movie_id}", response_model=Movie)
def update_movie(
        movie_id: int,
        movie_update: MovieUpdate,
        movie_service: MovieService = Depends(get_movie_service)
):
    movie = movie_service.update_movie(movie_id, movie_update)
    if not movie:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    return movie

@router.delete("/{movie_id}", status_code=204)
def delete_movie(movie_id: int, movie_service: MovieService = Depends(get_movie_service)):
    success = movie_service.delete_movie(movie_id)
    if not success:
        raise HTTPException(status_code = 404, detail="Фильм не найден")
    return None
