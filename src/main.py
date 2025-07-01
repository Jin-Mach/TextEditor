import pathlib
import sys

from PyQt6.QtCore import QTranslator, QLibraryInfo, QLocale
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from src.ui.main_window import MainWindow
from src.utilities.application_theme import ApplicationTheme
from src.utilities.data_provider import DataProvider

application_icon = pathlib.Path(__file__).parent.joinpath("icons", "applicationIcon.png")

def create_app() -> None:
    application = QApplication(sys.argv)
    if application_icon.exists():
        application.setWindowIcon(QIcon(str(application_icon)))
    os_language = QLocale().system().name()
    translator = QTranslator()
    translator_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
    if translator.load(f"qt_{os_language}", translator_path):
        application.installTranslator(translator)
    window = MainWindow(DataProvider.get_language_code())
    ApplicationTheme.set_light_theme(application, window)
    window.show()
    sys.exit(application.exec())