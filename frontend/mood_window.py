#xокно выбора настроения

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
)
from PyQt6.QtCore import pyqtSignal


class MoodWindow(QDialog):
    #Окно выбора настроения для рекомендаций фильмов.
    mood_selected = pyqtSignal(str)  # сигнал с выбранным настроением

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Выбор настроения")
        self.setFixedSize(400, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        label = QLabel("Какое у вас настроение?")
        label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 20px;")
        layout.addWidget(label)

        # Кнопки настроений
        moods = ["Радостное", "Грустное", "Энергичное", "Романтическое", "Задумчивое", "Страшное"]
        for mood in moods:
            btn = QPushButton(mood)
            btn.setMinimumHeight(40)
            btn.clicked.connect(lambda checked, m=mood: self.select_mood(m))
            layout.addWidget(btn)

        # Кнопка отмены
        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(self.close)
        layout.addWidget(cancel_btn)

    def select_mood(self, mood: str):
        #Выбор настроения и закрытие окна
        self.mood_selected.emit(mood)
        self.close()