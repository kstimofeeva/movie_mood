import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from database.database import Database

load_dotenv()

DATABASE_URL= ""

if not DATABASE_URL:
    print("DATABASE_URL не найден")
    exit(1)

movies_router=None
reviews_router=None
recommendations_router=None
API_ROUTERS_AVAILABLE=False

try:
    from api.routers.movies import router as movies_router
    from api.routers.reviews import router as reviews_router
    from api.routers.recommendations import router as recommendations_router

    API_ROUTERS_AVAILABLE = True
except ImportError as e:
    print("не удалось импортировать роутеры")
    API_ROUTERS_AVAILABLE = False

database = Database(DATABASE_URL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("запуск moviemood api")

    try:
        if database.test_connection():
            print("подключение успешно")
        else:
            print("не удалось подключиться к бд")
            raise ConnectionError("Database connection failed")

        database.create_tables()
        _add_test_data_if_empty()
    except Exception as e:
        print("ошибка при запуске")
        raise

    print("Moviemood API готов к работе")

    yield

app = FastAPI(
    title = "MovieMood API",
    description = "API для подбора фильмов по настроению",
    version='1.0.0',
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


def _add_test_data_if_empty():
    """Добавляет тестовые данные если база пустая"""
    try:
        from services.movie_service import MovieService
        from services.review_service import ReviewService
        from schemas.movie_schemas import MovieCreate

        session = database.get_session()
        try:
            movie_service = MovieService(session)

            # Просто проверяем есть ли фильмы
            existing_movies = movie_service.get_all_movies(limit=1)

            if not existing_movies:
                print("📝 Добавляем тестовые фильмы...")

                # ТОЛЬКО фильмы, без отзывов
                test_movies = [
                    MovieCreate(
                        title="Интерстеллар",
                        genre="фантастика",
                        description="Космическое путешествие через червоточину"
                    ),
                    MovieCreate(
                        title="Начало",
                        genre="фантастика",
                        description="Проникновение в сны для кражи идей"
                    ),
                ]

                for movie_data in test_movies:
                    try:
                        movie = movie_service.create_movie(movie_data)
                        print(f"     🎥 Добавлен фильм: {movie.title}")
                    except Exception as e:
                        print(f"     ⚠️  Не удалось добавить фильм: {e}")

            print("✅ Тестовые данные проверены")

        finally:
            session.close()

    except Exception as e:
        print(f"⚠️  Не удалось добавить тестовые данные: {e}")


@app.get("/")
def root():
    return {
        "message" : "Добро пожаловать в MovieMood API!",
        "version": "1.0.0",
        "structure": "Использует папку api для роутеров",
        "endpoints": {
            "health": "/health",
            "api_docs": "/docs",
            "movies": "/api/movies" if API_ROUTERS_AVAILABLE else "/movies",
            "reviews": "/api/reviews" if API_ROUTERS_AVAILABLE else "/reviews"
        }
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "databse": "connected" if database.test_connection() else "disconnected",
        "api_routers": "loaded" if API_ROUTERS_AVAILABLE else "not_found"
    }

if API_ROUTERS_AVAILABLE:
    app.include_router(movies_router, prefix="/api")
    app.include_router(reviews_router, prefix="/api")
    app.include_router(recommendations_router, prefix="/api")

    print("роутеры из папки подключены")
else:
    print("роутеры из папки не подключены")

    @app.get("/movies/")
    def get_movies_fallback():
        return {
            "message" : "роутеры не загружены. Проверьте папку /api"
        }

    @app.get("/reviews/")
    def get_reviews_fallback():
        return {
            "message": "роутеры не загружены. Проверьте папку /api"
        }

if __name__ == "__main__":
    if API_ROUTERS_AVAILABLE:
        uvicorn.run(
            "main:app",
            host='0.0.0.0',
            port=8000,
            reload=True,
            log_level="info"
        )

