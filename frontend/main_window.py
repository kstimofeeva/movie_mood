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

import requests


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

        self.clear_search_btn = QPushButton("Очистить")
        self.clear_search_btn.clicked.connect(self.clear_search)
        top_panel.addWidget(self.clear_search_btn)

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
        self.genre_combo.addItems([
            "Все", "Комедия", "Драма", "Боевик", "Фантастика",
            "Мелодрама", "Триллер", "Ужасы", "Мультфильм",
            "Документальный", "Другое"
        ])
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

        self.movie_count_label = QLabel("Фильмов: 0")
        main_layout.addWidget(self.movie_count_label)

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
        #self.load_movies()

    def load_movies(self):
        #загрузка фильмов в таблицу
        try:
            #запрос к API
            response = requests.get("http://localhost:8000/api/movies/")
            print(response)

            if response.status_code == 200:
                movies = response.json()

                # Отображаем фильмы в таблице
                self.movies_table.setRowCount(len(movies))
                for row, movie in enumerate(movies):
                    # ID
                    self.movies_table.setItem(row, 0, QTableWidgetItem(str(movie.get('id', ''))))

                    # Название
                    title_item = QTableWidgetItem(movie.get('title', 'Без названия'))
                    title_item.setFlags(title_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    self.movies_table.setItem(row, 1, title_item)

                    # Жанр
                    genre_item = QTableWidgetItem(movie.get('genre', 'Не указан'))
                    self.movies_table.setItem(row, 2, genre_item)

                    # Описание
                    description = movie.get('description', 'Нет описания')
                    if len(description) > 100:  # Обрезаем длинные описания
                        description = description[:100] + '...'
                    desc_item = QTableWidgetItem(description)
                    desc_item.setToolTip(movie.get('description', ''))  # Полное описание при наведении
                    self.movies_table.setItem(row, 3, desc_item)

                self.movies_table.resizeRowsToContents()

                # Обновляем статус
                self.movie_count_label.setText(f"Фильмов: {len(movies)}")

            elif response.status_code == 404:
                QMessageBox.information(self, "Информация",
                                        "Фильмов пока нет в базе. Добавьте первый фильм!")
            else:
                QMessageBox.warning(self, "Ошибка",
                                    f"Ошибка сервера: {response.status_code}")

        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Ошибка подключения",
                                 "Не удалось подключиться к серверу.\n"
                                 "Убедитесь, что бэкенд запущен на http://localhost:8000")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка при загрузке фильмов: {str(e)}")

    def on_search_clicked(self):
        """Обработка поиска фильмов через API"""
        search_text = self.search_input.text().strip()

        if not search_text:
            # Если поле пустое, показываем все фильмы
            self.load_movies()
            return

        try:
            # Ищем фильмы через API
            response = requests.get(
                "http://localhost:8000/api/movies/search/",
                params={'title': search_text}
            )

            if response.status_code == 200:
                movies = response.json()

                if movies:
                    self._display_search_results(movies)
                    QMessageBox.information(self, "Поиск",
                                            f"Найдено {len(movies)} фильмов по запросу: '{search_text}'")
                else:
                    QMessageBox.information(self, "Поиск",
                                            f"По запросу '{search_text}' ничего не найдено")
                    self.movies_table.setRowCount(0)
            else:
                QMessageBox.warning(self, "Ошибка",
                                    f"Ошибка при поиске: {response.status_code}")

        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Ошибка подключения",
                                 "Не удалось подключиться к серверу")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка при поиске: {str(e)}")

    def open_mood_window(self):
        #Открывает окно выбора настроения
        self.mood_window = MoodWindow(self)
        self.mood_window.mood_selected.connect(self.on_mood_selected)
        self.mood_window.show()

    def on_mood_selected(self, mood: str):
        """Обработка выбора настроения"""
        self.current_mood = mood
        self.mood_label.setText(f"Настроение: {mood}")

        # Маппинг настроений на жанры (временное решение)
        mood_to_genre = {
            "Радостное": "Комедия",
            "Грустное": "Драма",
            "Энергичное": "Боевик",
            "Романтическое": "Мелодрама",
            "Задумчивое": "Фантастика",
            "Страшное": "Триллер"
        }

        genre = mood_to_genre.get(mood, "")

        if genre:
            try:
                response = requests.get(
                    "http://localhost:8000/api/movies/search/",
                    params={'genre': genre}
                )

                if response.status_code == 200:
                    movies = response.json()

                    if movies:
                        self._display_search_results(movies)
                        QMessageBox.information(self, "Рекомендации",
                                                f"Подобраны фильмы для настроения: {mood}")
                    else:
                        QMessageBox.information(self, "Рекомендации",
                                                f"Нет фильмов для настроения '{mood}'")
                        self.load_movies()
                else:
                    QMessageBox.warning(self, "Ошибка",
                                        f"Ошибка при поиске рекомендаций")

            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка: {str(e)}")

    def on_genre_changed(self, genre: str):
        """Фильтрация фильмов по жанру"""
        if genre == "Все":
            self.load_movies()
            return

        try:
            # Ищем фильмы по жанру через API
            response = requests.get(
                "http://localhost:8000/api/movies/search/",
                params={'genre': genre}
            )

            if response.status_code == 200:
                movies = response.json()
                self._display_search_results(movies)
            else:
                QMessageBox.warning(self, "Ошибка",
                                    f"Ошибка при фильтрации: {response.status_code}")

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка при фильтрации: {str(e)}")

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

    def _display_search_results(self, movies):
        """Отображает результаты поиска"""
        self.movies_table.setRowCount(len(movies))

        for row, movie in enumerate(movies):
            self.movies_table.setItem(row, 0, QTableWidgetItem(str(movie.get('id', ''))))

            title_item = QTableWidgetItem(movie.get('title', ''))
            title_item.setFlags(title_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.movies_table.setItem(row, 1, title_item)

            self.movies_table.setItem(row, 2, QTableWidgetItem(movie.get('genre', '')))

            description = movie.get('description', '')
            if len(description) > 100:
                description = description[:100] + '...'
            desc_item = QTableWidgetItem(description)
            desc_item.setToolTip(movie.get('description', ''))
            self.movies_table.setItem(row, 3, desc_item)

        self.movies_table.resizeRowsToContents()
        self.movie_count_label.setText(f"Найдено: {len(movies)}")

    def clear_search(self):
        """Очищает поиск и показывает все фильмы"""
        self.search_input.clear()
        self.load_movies()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())