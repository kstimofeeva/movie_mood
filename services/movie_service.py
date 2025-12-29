from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from database.models import Movie
from schemas.movie_schemas import MovieCreate, MovieUpdate
from sqlalchemy import and_
class MovieService:
    def __init__(self, db: Session):
        self.db = db

#добавление фильма в бд
    def create_movie(self, movie_data: MovieCreate) -> Movie:
        try:
            db_movie = Movie (
                title = movie_data.title,
                genre = movie_data.genre,
                description = movie_data.description
            )
            self.db.add(db_movie)
            self.db.commit()
            self.db.refresh(db_movie)
            return db_movie
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Фильм с таким названием уже существует или нарушена целостность данных")
        except SQLAlchemyError:
            self.db.rollback()
            raise Exception("Ошибка при сохранении фильмов в БД")
        except Exception:
            self.db.rollback()
            raise Exception("Ошибка сервера")

    #получение фильма по айдишнику
    def get_movie(self, movie_id: int) -> Movie:
        try:
            movie = self.db.query(Movie).filter(Movie.id == movie_id).first()
            return movie
        except SQLAlchemyError:
            raise Exception("Ошибка при получении данных")
        except Exception:
            raise Exception("Ошибка сервера")

    def get_all_movies(self, skip: int = 0, limit: int = 100):
        try:
            movies = self.db.query(Movie).offset(skip).limit(limit).all()
            return movies
        except  SQLAlchemyError:
            raise Exception("Ошибка при получении данных")
        except Exception:
            raise Exception("Ошибка сервера")

    #поиск фильма по названию / жанру
    def search_movies(self, title: str = None, genre: str = None):
        try:
            query = self.db.query(Movie)
            if title and genre:
                query = query.filter(and_(Movie.title.ilike(f"%{title}%"), Movie.genre.ilike(f"%{genre}%")))
            elif title:
                query = query.filter(Movie.title.ilike(f"%{title}%"))
            elif genre:
                query = query.filter(Movie.genre.ilike(f"%{genre}%"))
            return query.all()
        except SQLAlchemyError:
            raise Exception("Ошибка при поиске фильмов в БД")
        except Exception:
            raise Exception("Ошибка сервера")
    #фильм по настроению
    def get_movies_by_mood(self, mood: str):
        try:
            if not mood:
                raise ValueError("Не указано настроение для фильма")
            return self.db.query(Movie).filter(Movie.mood.ilike(f"%{mood}%")).all()
        except SQLAlchemyError:
            raise Exception("Ошибка при поиске фильмов по настроению")
        except Exception:
            raise Exception("Ошибка сервера")
    #обновление инфы о фильме
    def update_movie(self, movie_id: int, movie_data: MovieUpdate):
        try:
            movie = self.get_movie(movie_id)
            if not movie:
                raise ValueError(f"Фильм с ID {movie_id} не найден:(")

            upd_data = movie_data.model_dump(exclude_unset = True)

            if not upd_data:
                raise ValueError("Не переданы данные для обновления информации о фильме")

            for field, value in upd_data.items():
                setattr(movie, field, value)

            self.db.commit()
            self.db.refresh(movie)
            return movie

        except ValueError as e:
            self.db.rollback()
            raise e
        except SQLAlchemyError:
            self.db.rollback()
            raise Exception("Ошибка при обновлении фильма в бд")
        except Exception:
            self.db.rollback()
            raise Exception("Внутренняя ошибка сервера")

    def delete_movie(self, movie_id: int) -> bool:
        try:
            movie = self.get_movie(movie_id)
            if not movie:
                return False
            self.db.delete(movie)
            self.db.commit()
            return True
        except SQLAlchemyError:
            self.db.rollback()
            raise Exception("Ошибка при удалении фильма из БД")
        except Exception:
            self.db.rollback()
            raise Exception("Ошибка сервера")