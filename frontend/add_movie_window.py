# окно добавления фильма

from services.movie_service import MovieService

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTextEdit, QComboBox, QPushButton, QMessageBox
)
from PyQt6.QtCore import pyqtSignal
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from services.movie_service import MovieService
    from schemas.movie_schemas import MovieCreate
    from database.database import Database
    DATABASE_URL = ""

    database = Database(DATABASE_URL)
    BACKEND_AVAILABLE = True
except ImportError as e:
    print(f"Бэкенд не доступен: {e}")
    BACKEND_AVAILABLE = False
    database = None

class AddMovieWindow(QDialog):
    #Окно добавления нового фильма.

    movie_added = pyqtSignal(dict)  # сигнал с данными фильма

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить фильм")
        self.setFixedSize(500, 400)

        self.db_session = None
        if BACKEND_AVAILABLE and database:
            self.db_session = database.get_session()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Название
        layout.addWidget(QLabel("Название фильма:"))
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Введите название...")
        layout.addWidget(self.title_input)

        # Жанр
        layout.addWidget(QLabel("Жанр:"))
        self.genre_combo = QComboBox()
        self.genre_combo.addItems([
            "Комедия", "Драма", "Боевик", "Фантастика", "Мелодрама",
            "Триллер", "Ужасы", "Мультфильм", "Документальный", "Другое"
        ])
        layout.addWidget(self.genre_combo)

        # Описание
        layout.addWidget(QLabel("Описание:"))
        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(100)
        layout.addWidget(self.desc_input)

        # Кнопки
        button_layout = QHBoxLayout()
        self.add_btn = QPushButton("Добавить")
        self.add_btn.clicked.connect(self.add_movie)
        button_layout.addWidget(self.add_btn)

        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(self.close)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)

    def add_movie(self):
        #проверка на подключение к бд
        # try:
        #     if database.test_connection():
        #         print(f"   ✅ УСПЕХ!")
        #         print("   Создаем таблицы...")
        #         if database.create_tables():
        #             print("   ✅ Таблицы созданы")
        #         else:
        #             print("   ❌ Не удалось создать таблицы")
        #     else:
        #         print(f"   ❌ БД  не существует или ошибка подключения")
        # except Exception as e:
        #     print(f"   ❌ Ошибка: {str(e)[:50]}...")

        title = self.title_input.text().strip()
        genre = self.genre_combo.currentText()
        desc = self.desc_input.toPlainText().strip()

        if not title:
            QMessageBox.warning(self, "Ошибка", "Введите название фильма")
            return

        if not genre:
            QMessageBox.warning(self, "Ошибка", "Введите жанр фильма")
            self.genre_combo.setFocus()
            return

        self.add_btn.setEnabled(False)
        self.add_btn.setText("Добавление...")

        try:
            if BACKEND_AVAILABLE and self.db_session:
                #сервис + добавляем фильм в БД
                movie_service = MovieService(self.db_session)
                movie_data = MovieCreate(
                    title=title,
                    genre=genre,
                    description=desc
                )
                # сохранить в бд
                created_movie = movie_service.create_movie(movie_data)

                movie_dict = {
                    "id": created_movie.id,
                    "title": created_movie.title,
                    "genre": created_movie.genre,
                    "description": created_movie.description
                }


                # Отправляем сигнал с реальными данными из БД
                self.movie_added.emit(movie_dict)
                QMessageBox.information(self, "Успех", f"Фильм '{title}' добавлен!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить фильм: {str(e)}")

        finally:
            self.add_btn.setEnabled(True)
            self.add_btn.setText("Добавить")

            # Закрываем соединение с БД
            if self.db_session:
                self.db_session.close()
