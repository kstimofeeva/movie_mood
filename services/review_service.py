from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from database.models import Movie, Review
from schemas.review_schemas import ReviewCreate
from ml.sentiment_analyzer import analyzer


class ReviewService:
    def __init__(self, db: Session):
        self.db = db
        self.analyzer = analyzer

    #создание отзыва
    def create_review(self, review_data: ReviewCreate) -> Review:
        try:
            if not review_data.review_text or not review_data.review_text.strip():
                raise ValueError('Текст отзыва не может быть пустым')
            if not isinstance(review_data.movie_id, int) or review_data.movie_id <= 0:
                raise ValueError("Неверное значение ID фильма")

            movie = self.db.query(Movie).filter(Movie.id == review_data.movie_id).first()

            if not movie:
                raise ValueError (f"Такого фильма с ID {review_data.movie_id} не существует")

            sentiment_result  = self.analyzer.predict(review_data.review_text)

            db_review = Review(
                movie_id = review_data.movie_id,
                review_text = review_data.review_text,
                sentiment = sentiment_result['sentiment'],
                sentiment_score = sentiment_result['score']
            )
            self.db.add(db_review)
            self.db.commit()
            self.db.refresh(db_review)

            self._update_movie_mood(review_data.movie_id)

            return db_review
        except ValueError as e:
            self.db.rollback()
            raise e
        except IntegrityError:
            self.db.rollback()
            raise Exception("Ошибка при сохранении отзыва в БД")
        except SQLAlchemyError:
            self.db.rollback()
            raise Exception("Ошибка БД при создании отзыва")
        except Exception:
            self.db.rollback()
            raise Exception("Внутренняя ошибка сервера")

    #внутренняя функция без вызова исключений. true если норм обновилось настроение, false если где-то кринжанули (ни на что не влияет)
    def _update_movie_mood(self, movie_id: int) -> bool:
        try:
            reviews = self.db.query(Review).filter(Review.movie_id == movie_id).all()
            if not reviews:
                return False
            positive_count = sum(1 for i in reviews if i.sentiment == 'positive')
            negative_count = sum(1 for i in reviews if i.sentiment == 'negative')
            reviews_count = len(reviews)

            movie = self.db.query(Movie).filter(Movie.id == movie_id).first()

            if not movie:
                return False

            #хз какая логика определения настроения у нас, пусть такая будет
            if reviews_count == 0:
                movie.mood = None
            elif positive_count >= 0.75 * reviews_count:
                movie.mood = 'positive'
            elif negative_count >= 0.75 * reviews_count:
                movie.mood = 'negative'
            else:
                movie.mood = 'neutral'

            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    #список всех отзывов
    def get_reviews_by_movie(self, movie_id: int):
        try:
            if not isinstance(movie_id, int) or movie_id <= 0:
                raise ValueError("Неверное значение для ID фильма")

            return self.db.query(Review).filter(Review.movie_id == movie_id).all()
        except ValueError as e:
            raise e
        except SQLAlchemyError:
            raise Exception("Ошибка при получении отзыва из БД")
        except Exception:
            raise Exception("Ошибка сервера")

    def get_review(self, review_id: int) -> Review:
        try:
            if not isinstance(review_id, int) or review_id <= 0:
                raise ValueError("Неверное значение ID отзыва")
            return self.db.query(Review).filter(Review.id == review_id).first()
        except ValueError as e:
            raise e
        except SQLAlchemyError:
            raise Exception("Ошибка получения отзыва из бд")
        except Exception:
            raise Exception("Внутренняя ошибка сервера")

    def delete_review(self, review_id: int) -> bool:
        try:
            if not isinstance(review_id, int) or review_id <= 0:
                raise ValueError("Неверный ID отзыва")

            review = self.db.query(Review).filter(Review.id == review_id).first()
            if not review:
                return False
            movie_id = review.movie_id
            self.db.delete(review)
            self.db.commit()

            self._update_movie_mood(movie_id)
            return True
        except ValueError as e:
            self.db.rollback()
            raise e
        except SQLAlchemyError:
            self.db.rollback()
            raise Exception("Ошибка при удалении отзыва из бд")
        except Exception:
            self.db.rollback()
            raise Exception("Внутренняя ошибка сервера")
