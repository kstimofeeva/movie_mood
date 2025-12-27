#главное окно приложения

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QLabel, QMessageBox, QComboBox
)
from PyQt6.QtCore import Qt
from .mood_window import MoodWindow
from .add_movie_window import AddMovieWindow
from .add_review_window import AddReviewWindow


class MainWindow(QMainWindow):
    #главное окно (поиск, выбор настроения, таблицу фильмов, кнопка действий)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Movie Mood Recommender")
        self.setGeometry(100, 100, 900, 600)

        self.current_mood = None  #хранит выбранное настроение
        self.init_ui()

    def init_ui(self):
        # центральный виджет и основной layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        #Панель поиска и настроения
        top_panel = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите название фильма...")
        self.search_input.setMinimumHeight(30)
        top_panel.addWidget(self.search_input)

        self.search_btn = QPushButton("Поиск")
        self.search_btn.clicked.connect(self.on_search_clicked)
        top_panel.addWidget(self.search_btn)

        self.mood_btn = QPushButton("Выбрать настроение")
        self.mood_btn.clicked.connect(self.open_mood_window)
        top_panel.addWidget(self.mood_btn)

        self.mood_label = QLabel("Настроение: не выбрано")
        top_panel.addWidget(self.mood_label)

        main_layout.addLayout(top_panel)

        #Фильтр по жанру
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Жанр:"))
        self.genre_combo = QComboBox()
        self.genre_combo.addItems(["Все", "Комедия", "Драма", "Боевик", "Фантастика", "Мелодрама", "Триллер"])
        self.genre_combo.currentTextChanged.connect(self.on_genre_changed)
        filter_layout.addWidget(self.genre_combo)
        filter_layout.addStretch()
        main_layout.addLayout(filter_layout)

        #Таблица фильмов
        self.movies_table = QTableWidget()
        self.movies_table.setColumnCount(4)
        self.movies_table.setHorizontalHeaderLabels(["ID", "Название", "Жанр", "Описание"])
        self.movies_table.horizontalHeader().setStretchLastSection(True)
        main_layout.addWidget(self.movies_table)

        #Панель кнопок
        button_layout = QHBoxLayout()

        self.add_movie_btn = QPushButton("Добавить фильм")
        self.add_movie_btn.clicked.connect(self.open_add_movie_window)
        button_layout.addWidget(self.add_movie_btn)

        self.add_review_btn = QPushButton("Добавить отзыв")
        self.add_review_btn.clicked.connect(self.open_add_review_window)
        button_layout.addWidget(self.add_review_btn)

        self.refresh_btn = QPushButton("Обновить список")
        self.refresh_btn.clicked.connect(self.load_movies)
        button_layout.addWidget(self.refresh_btn)

        self.exit_btn = QPushButton("Выход")
        self.exit_btn.clicked.connect(self.close)
        button_layout.addWidget(self.exit_btn)

        main_layout.addLayout(button_layout)

        # Заглушка данных для демонстрации
        self.load_demo_movies()

    def load_demo_movies(self):
        #Заглушка: загрузка демо-фильмов в таблицу
        demo_movies = [
            (1, "Интерстеллар", "Фантастика", "Путешествие через червоточину для спасения человечества."),
            (2, "Король Лев", "Мультфильм", "История о взрослении львёнка Симбы."),
            (3, "Титаник", "Драма", "Любовная история на фоне крушения корабля."),
        ]
        self.movies_table.setRowCount(len(demo_movies))
        for row, (id_, title, genre, desc) in enumerate(demo_movies):
            self.movies_table.setItem(row, 0, QTableWidgetItem(str(id_)))
            self.movies_table.setItem(row, 1, QTableWidgetItem(title))
            self.movies_table.setItem(row, 2, QTableWidgetItem(genre))
            self.movies_table.setItem(row, 3, QTableWidgetItem(desc))

    def on_search_clicked(self):
        #Обработка поиска (заглушка)
        text = self.search_input.text()
        QMessageBox.information(self, "Поиск", f"Ищем фильмы по запросу: '{text}'")
        # Здесь будет вызов API поиска

    def open_mood_window(self):
        #Открывает окно выбора настроения
        self.mood_window = MoodWindow(self)
        self.mood_window.mood_selected.connect(self.on_mood_selected)
        self.mood_window.show()

    def on_mood_selected(self, mood: str):
        #Обработка выбора настроения
        self.current_mood = mood
        self.mood_label.setText(f"Настроение: {mood}")
        QMessageBox.information(self, "Настроение выбрано", f"Подбираем фильмы для настроения: {mood}")
        # Здесь будет вызов API для рекомендаций по настроению

    def on_genre_changed(self, genre: str):
        #Обработка изменения жанра (заглушка)
        if genre != "Все":
            QMessageBox.information(self, "Фильтр", f"Фильтруем по жанру: {genre}")
        # Здесь будет вызов API фильтрации

    def open_add_movie_window(self):
        #Открывает окно добавления фильма
        self.add_movie_window = AddMovieWindow(self)
        self.add_movie_window.movie_added.connect(self.on_movie_added)
        self.add_movie_window.show()

    def on_movie_added(self, movie_data: dict):
        """Обработка добавления фильма"""
        self.load_movies()

        if 'id' in movie_data:
            QMessageBox.information(self, "Успех", f"Фильм добавлен! ID: {movie_data['id']}")

    def open_add_review_window(self):
        #Открывает окно добавления отзыва
        selected_row = self.movies_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите фильм из таблицы")
            return
        movie_id = self.movies_table.item(selected_row, 0).text()
        movie_title = self.movies_table.item(selected_row, 1).text()
        self.add_review_window = AddReviewWindow(self, movie_id, movie_title)
        self.add_review_window.review_added.connect(self.on_review_added)
        self.add_review_window.show()

    def on_review_added(self, review_data: dict):
        #Обработка добавления отзыва (заглушка)
        QMessageBox.information(self, "Отзыв добавлен", f"Добавлен отзыв: {review_data}")

    def load_movies(self):
        #Заглушка: загрузка фильмов (потом будет API)
        self.load_demo_movies()
        QMessageBox.information(self, "Обновление", "Список фильмов обновлён")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())