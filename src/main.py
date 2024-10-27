import pathlib
import sys

from PyQt6.QtWidgets import QApplication

from src.ui.main_window import MainWindow
from src.utilities.logging_manager import setup_logger
from src.utilities.messagebox_manager import MessageboxManager

def create_app() -> None:
    application = QApplication(sys.argv)

    style_file_path = pathlib.Path(__file__).parent.joinpath("style", "styles.qss")
    try:
        with open(style_file_path, "r") as file:
            application.setStyleSheet(file.read())
    except Exception as e:
        setup_logger().error(str(e))
        MessageboxManager.show_load_error_message(str(style_file_path))

    window = MainWindow()
    window.show()
    sys.exit(application.exec())