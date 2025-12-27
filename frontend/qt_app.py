import sys
from PyQt6.QtWidgets import QApplication
from .main_window import MainWindow


def run_qt_app():
    #Запуск Qt-приложения
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # современный стиль

    window = MainWindow()
    window.show()


    sys.exit(app.exec())


if __name__ == "__main__":
    run_qt_app()