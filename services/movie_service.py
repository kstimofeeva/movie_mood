from sqlalchemy.orm import Session
from database.models import Movie
from schemas.movie_schemas import MovieCreate, MovieUpdate

class MovieService:
    def __init__(self, db: Session):
        self.db = db

#добавление фильма в бд
    def create_movie(self, movie_data: MovieCreate) -> Movie:
        db_movie = Movie (
            title = movie_data.title,
            genre = movie_data.genre,
            description = movie_data.description
        )

        self.db.add(db_movie)
        self.db.commit()
        self.db.refresh(db_movie)
        return db_movie

    #получение фильма по айдишнику
    def get_movie(self, movie_id: int) -> Movie:
        return self.db.query(Movie).filter(Movie.id == movie_id).first()

    #поиск фильма по названию / жанру
    def search_movies(self, title: str = None, genre: str = None):
        query = self.db.query(Movie)
        if title and genre:
            query = query.filter(Movie.title.ilike(f"%{title}%") and Movie.genre.ilike(f"{genre}"))
        elif title:
            query = query.filter(Movie.title.ilike(f"%{title}%"))
        elif genre:
            query = query.filter(Movie.genre.ilike(f"%{genre}%"))
        return query.all()

    #фильм по настроению
    def get_movies_by_mood(self, mood: str):
        return self.db.query(Movie).filter(Movie.mood.ilike(f"%{mood}%")).all()

    #обновление инфы о фильме
    def update_movie(self, movie_id: int, movie_data: MovieUpdate):
        try:
            movie = self.get_movie(movie_id)
            if not movie:
                raise ValueError(f"Фильм с ID {movie_id} не найден:(")

            upd_data = movie_data.model_dump(exclude_unset = True)

            if not upd_data:
                raise ValueError("Не переданы данные для обновления информации о фильме")

            for fields, value in upd_data.items():
                setattr(movie, fields, value)

            self.db.commit()
            self.db.refresh(movie)
            return movie

        except Exception:
            self.db.rollback()
            raise Exception
