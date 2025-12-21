# окно добавления фильма

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTextEdit, QComboBox, QPushButton, QMessageBox
)
from PyQt6.QtCore import pyqtSignal


class AddMovieWindow(QDialog):
    #Окно добавления нового фильма.

    movie_added = pyqtSignal(dict)  # сигнал с данными фильма

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить фильм")
        self.setFixedSize(500, 400)
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
        add_btn = QPushButton("Добавить")
        add_btn.clicked.connect(self.add_movie)
        button_layout.addWidget(add_btn)

        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(self.close)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)

    def add_movie(self):
        #Добавление фильма (заглушка)
        title = self.title_input.text().strip()
        genre = self.genre_combo.currentText()
        desc = self.desc_input.toPlainText().strip()

        if not title:
            QMessageBox.warning(self, "Ошибка", "Введите название фильма")
            return

        movie_data = {
            "title": title,
            "genre": genre,
            "description": desc
        }
        self.movie_added.emit(movie_data)
        self.close()