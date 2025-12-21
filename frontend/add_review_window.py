# окно добавления отзыва

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QMessageBox
)
from PyQt6.QtCore import pyqtSignal


class AddReviewWindow(QDialog):
    #Окно добавления отзыва

    review_added = pyqtSignal(dict)  # сигнал с данными отзыва

    def __init__(self, parent=None, movie_id=None, movie_title=None):
        super().__init__(parent)
        self.movie_id = movie_id
        self.movie_title = movie_title
        self.setWindowTitle(f"Отзыв к фильму: {movie_title}")
        self.setFixedSize(500, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel(f"Фильм: {self.movie_title} (ID: {self.movie_id})"))
        layout.addWidget(QLabel("Текст отзыва:"))

        self.review_input = QTextEdit()
        self.review_input.setPlaceholderText("Введите ваш отзыв...")
        layout.addWidget(self.review_input)

        button_layout = QHBoxLayout()
        add_btn = QPushButton("Добавить отзыв")
        add_btn.clicked.connect(self.add_review)
        button_layout.addWidget(add_btn)

        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(self.close)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)

    def add_review(self):
        #Добавление отзыва (заглушка)
        text = self.review_input.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Ошибка", "Введите текст отзыва")
            return

        review_data = {
            "movie_id": self.movie_id,
            "review_text": text,
            "sentiment": "auto"  # будет определено ML-моделью
        }
        self.review_added.emit(review_data)
        self.close()