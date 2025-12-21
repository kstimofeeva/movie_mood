# виджет списка фильмов

from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt


class MovieItemWidget(QWidget):
    #Виджет элемента фильма в списке
    def __init__(self, movie_id, title, genre, description):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        title_label = QLabel(f"<b>{title}</b>")
        title_label.setStyleSheet("font-size: 14px; color: #333;")
        layout.addWidget(title_label)

        genre_label = QLabel(f"Жанр: {genre}")
        genre_label.setStyleSheet("color: #666;")
        layout.addWidget(genre_label)

        desc_label = QLabel(description[:100] + "..." if len(description) > 100 else description)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #777; font-size: 12px;")
        layout.addWidget(desc_label)


class MovieListWidget(QListWidget):
    #Кастомный список фильмов с красивым отображением
    def __init__(self):
        super().__init__()
        self.setAlternatingRowColors(True)
        self.setStyleSheet("""
            QListWidget::item {
                border-bottom: 1px solid #ddd;
                padding: 5px;
            }
            QListWidget::item:hover {
                background-color: #f0f0f0;
            }
        """)

    def add_movie(self, movie_id, title, genre, description):
        item = QListWidgetItem(self)
        widget = MovieItemWidget(movie_id, title, genre, description)
        item.setSizeHint(widget.sizeHint())
        self.addItem(item)
        self.setItemWidget(item, widget)