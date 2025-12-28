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
        skip: int = Query(0, ge=0, description="Пропустить первые N записей"),
        limit: int = Query(100, ge=1, le=100, description="Лимит записей"),
        movie_service: MovieService = Depends(get_movie_service)
):
    try:
        return movie_service.get_all_movies(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ошибка при получении фильмов")

@router.get("/{movie_id}", response_model=Movie)
def get_movie(movie_id: int, movie_service: MovieService = Depends(get_movie_service)):
    try:
        movie = movie_service.get_movie(movie_id)
        if not movie:
            raise HTTPException(status_code=404, detail="Фильм не найден")
        return movie
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении фильма. {e}")

@router.get("/search/", response_model=List[Movie])
def search_movies(
        title: Optional[str] = Query(None, description="Поиск по названию"),
        genre: Optional[str] = Query(None, description="Поиск по жанру"),
        #mood: Optional[str] = Query(None, description="Поиск по настроению"),
        movie_service: MovieService = Depends(get_movie_service)
):
    try:
        return movie_service.search_movies(title=title, genre=genre)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ошибка при поиске фильмов")

'''
@router.get("/mood/{mood}", response_model=List[Movie])
def get_movies_by_mood(
        mood: str,
        movie_service: MovieService = Depends(get_movie_service)
):
    try:
        movies = movie_service.get_movies_by_mood(mood)
        return movies
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ошибка при поиске фильмов по настроению")
'''

@router.patch("/{movie_id}", response_model=Movie)
def update_movie(
        movie_id: int,
        movie_update: MovieUpdate,
        movie_service: MovieService = Depends(get_movie_service)
):
    try:
        movie = movie_service.update_movie(movie_id, movie_update)
        return movie
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ошибка при обновлении фильма")

@router.delete("/{movie_id}", status_code=204)
def delete_movie(movie_id: int, movie_service: MovieService = Depends(get_movie_service)):
    try:
        success = movie_service.delete_movie(movie_id)
        if not success:
            raise HTTPException(status_code = 404, detail="Фильм не найден")
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ошибка при удалении фильма")

