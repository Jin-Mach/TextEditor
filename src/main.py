import pathlib
import sys

from PyQt6.QtWidgets import QApplication

from src.ui.main_window import MainWindow
from src.utilities.application_theme import ApplicationTheme

style_file_path = pathlib.Path(__file__).parent.joinpath("style", "styles.qss")

def create_app() -> None:
    application = QApplication(sys.argv)
    ApplicationTheme.set_light_theme(application, style_file_path)
    window = MainWindow()
    window.show()
    sys.exit(application.exec())