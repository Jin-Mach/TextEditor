import pathlib
import sys

from PyQt6.QtWidgets import QApplication

from src.ui.main_window import MainWindow
from src.utilities.application_theme import ApplicationTheme
from src.utilities.data_provider import DataProvider

def create_app() -> None:
    application = QApplication(sys.argv)
    window = MainWindow(DataProvider.get_language_code())
    ApplicationTheme.set_light_theme(application, window)
    window.show()
    sys.exit(application.exec())