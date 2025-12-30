# окно добавления отзыва

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QMessageBox
)

import requests
from PyQt6.QtCore import QThread, pyqtSignal


class ReviewSubmitThread(QThread):
    #Поток для асинхронной отправки отзыва
    finished = pyqtSignal(dict, str)  # сигнал: (данные_ответа, ошибка)

    def __init__(self, api_url, review_data):
        super().__init__()
        self.api_url = api_url
        self.review_data = review_data

    def run(self):
        try:
            response = requests.post(
                f"{self.api_url}/reviews/",
                json=self.review_data,
                timeout=10
            )
            response.raise_for_status()
            self.finished.emit(response.json(), "")
        except requests.exceptions.RequestException as e:
            self.finished.emit({}, f"Ошибка: {str(e)}")


class AddReviewWindow(QDialog):
    #Окно добавления отзыва

    review_added = pyqtSignal(dict)  # сигнал с данными отзыва

    def __init__(self, parent=None, movie_id=None, movie_title=None, api_url="http://localhost:8000"):
        super().__init__(parent)
        self.movie_id = movie_id
        self.movie_title = movie_title
        self.api_url = api_url
        self.setWindowTitle(f"Отзыв к фильму: {movie_title}")
        self.setFixedSize(500, 300)
        self.init_ui()

        self.review_input = None
        self.add_btn = None
        self.cancel_btn = None
        self.progress_bar = None

        self.setWindowTitle(f"Отзыв к фильму: {movie_title}")
        self.setFixedSize(500, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel(f"Фильм: {self.movie_title} (ID: {self.movie_id})"))
        layout.addWidget(QLabel("Текст отзыва:"))

        self.review_input = QTextEdit()
        self.review_input.setPlaceholderText("Введите ваш отзыв...")
        self.review_input.setMaximumHeight(150)
        layout.addWidget(self.review_input)

        button_layout = QHBoxLayout()

        self.add_btn = QPushButton("Добавить отзыв")
        self.add_btn.clicked.connect(self.add_review)
        button_layout.addWidget(self.add_btn)

        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.clicked.connect(self.close)
        button_layout.addWidget(self.cancel_btn)

        layout.addLayout(button_layout)

    def add_review(self):
        text = self.review_input.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Ошибка", "Введите текст отзыва")
            return

        self.add_btn.setEnabled(False)
        self.cancel_btn.setEnabled(False)
        self.progress_bar.setVisible(True)

        review_data = {
            "movie_id": self.movie_id,
            "review_text": text,
        }
        self.thread = ReviewSubmitThread(self.api_url, review_data)
        self.thread.finished.connect(self.on_review_submitted)
        self.thread.start()

    def on_review_submitted(self, response_data, error):
        #Обработка отправки
        if self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()

        self.add_btn.setEnabled(True)
        self.cancel_btn.setEnabled(True)
        self.progress_bar.setVisible(False)

        if error:
            QMessageBox.critical(self, "Ошибка",
                                 f"Не удалось добавить отзыв:\n{error}")
        else:
            QMessageBox.information(self, "Успех", "Отзыв успешно добавлен!")

            self.review_added.emit(response_data)
            self.close()
