import json
import pathlib

from PyQt6.QtCore import QLocale

from src.ui.dialogs.error_dialog_manager import ErrorDialogManager
from src.utilities.logging_manager import setup_logger


class DataProvider:

    @staticmethod
    def get_language_code() -> str:
        try:
            language = QLocale.system().name()
            language_directory = pathlib.Path(__file__).parent.parent.joinpath("config")
            if not DataProvider.check_empty_dir(language_directory.joinpath(language)):
                return DataProvider.get_supported_languages()
            language_folders = []
            for folder in language_directory.iterdir():
                if folder.is_dir():
                    language_folders.append(folder.name)
            if language not in language_folders:
                language = DataProvider.get_supported_languages()
            return language
        except Exception as e:
            DataProvider.exception_handler(e)

    @staticmethod
    def get_tooltips(widget_tooltip: str, language_code: str) -> dict:
        try:
            with open(str(pathlib.Path(__file__).parent.parent.joinpath("config", language_code, "tooltips.json")), "r", encoding="utf-8") as file:
                tooltips = json.load(file)[widget_tooltip]
                return tooltips
        except Exception as e:
            DataProvider.exception_handler(e)

    @staticmethod
    def get_icons(icons_path: pathlib.Path) -> dict:
        try:
            icons_dict = {}
            for icon in icons_path.iterdir():
                if icon.is_file() and icon.suffix == ".png":
                    key = icon.stem
                    icons_dict[key] = icon
            return icons_dict
        except Exception as e:
            DataProvider.exception_handler(e)

    @staticmethod
    def get_errors(language_code: str) -> dict:
        try:
            with open(str(pathlib.Path(__file__).parent.parent.joinpath("config", language_code, "errors.json")), "r", encoding="utf-8") as file:
                errors = json.load(file)
                return errors
        except Exception as e:
            DataProvider.exception_handler(e)

    @staticmethod
    def get_ui_text(widget_tooltip: str, language_code: str) -> dict:
        try:
            with open(str(pathlib.Path(__file__).parent.parent.joinpath("config", language_code, "ui_text.json")), "r", encoding="utf-8") as file:
                ui_text = json.load(file)[widget_tooltip]
                return ui_text
        except Exception as e:
            DataProvider.exception_handler(e)

    @staticmethod
    def get_supported_languages() -> str:
        try:
            supported_languages = []
            language_dir = pathlib.Path(__file__).parent.parent.joinpath("config")
            for folder in language_dir.iterdir():
                if folder.is_dir:
                    if DataProvider.check_empty_dir(folder):
                        supported_languages.append(folder.name)
            dialog = ErrorDialogManager()
            language = dialog.show_language_error_dialog(supported_languages)
            return language
        except Exception as e:
            DataProvider.exception_handler(e)

    @staticmethod
    def check_empty_dir(folder: pathlib.Path) -> bool:
        try:
            required_files = ["errors.json", "language_info.json", "tooltips.json", "ui_text.json"]
            for file in required_files:
                file_path = folder.joinpath(file)
                if not file_path.exists():
                    return False
                if file_path.stat().st_size == 0:
                    return False
            return True
        except Exception as e:
            DataProvider.exception_handler(e)

    @staticmethod
    def exception_handler(exception: Exception) -> None:
        logger = setup_logger()
        logger.error("An error occurred: %s", exception, exc_info=True)
        dialog = ErrorDialogManager()
        dialog.show_simple_error_messagebox(exception)