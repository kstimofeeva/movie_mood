from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

import sys
from PyQt6.QtWidgets import QApplication
from frontend.main_window import MainWindow

# Загружаем переменные из .env файла
load_dotenv()

app = FastAPI(
    title="Movie Mood API",
    description="API для подбора фильмов по настроению",
    version="1.0.0"
)

# CORS для PyQt приложения
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    # Показываем, что переменные загружены
    db_url = os.getenv("DATABASE_URL", "не установлена")
    return {
        "message": "Movie Mood API работает!",
        "database": db_url,
        "port": os.getenv("PORT", "8000"),
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    # Берём настройки из .env
    # host = os.getenv("HOST", "0.0.0.0")
    # port = int(os.getenv("PORT", 8000))

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)