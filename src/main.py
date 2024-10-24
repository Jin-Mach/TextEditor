import pathlib
import sys

from PyQt6.QtWidgets import QApplication

from src.ui.main_window import MainWindow

def create_app():
    application = QApplication(sys.argv)
    try:
        with open(str(pathlib.Path(__file__).parent.joinpath("ui", "styles.qss")), "r") as file:
            application.setStyleSheet(file.read())
    except Exception as e:
        print(f"Error: {e}")
    window = MainWindow()
    window.show()
    sys.exit(application.exec())