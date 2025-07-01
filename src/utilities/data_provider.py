import json
import pathlib

from PyQt6.QtCore import QLocale
from src.ui.dialogs.error_dialog_manager import ErrorDialogManager
from src.utilities.logging_manager import setup_logger


class DataProvider:
    config_path = pathlib.Path(__file__).parent.parent.joinpath("config")

    @staticmethod
    def get_language_code() -> str | None:
        try:
            language = QLocale.system().name()
            if not DataProvider.config_path.exists():
                return None

            language_directory = DataProvider.config_path
            if not DataProvider.check_empty_dir(language_directory.joinpath(language)):
                return DataProvider.get_supported_languages()

            language_folders = [folder.name for folder in language_directory.iterdir() if folder.is_dir()]
            if language not in language_folders:
                language = DataProvider.get_supported_languages()

            return language
        except Exception as e:
            DataProvider.exception_handler(e)
            return None

    @staticmethod
    def get_tooltips(widget_tooltip: str, language_code: str) -> dict | None:
        try:
            file_path = DataProvider.config_path.joinpath(language_code, "tooltips.json")
            if not file_path.exists():
                return None
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file).get(widget_tooltip)
        except Exception as e:
            DataProvider.exception_handler(e)
            return None

    @staticmethod
    def get_icons(icons_path: pathlib.Path) -> dict | None:
        try:
            if not icons_path.exists():
                return None
            icons_dict = {}
            for icon in icons_path.iterdir():
                if icon.is_file() and icon.suffix == ".png":
                    icons_dict[icon.stem] = icon
            return icons_dict
        except Exception as e:
            DataProvider.exception_handler(e)
            return None

    @staticmethod
    def get_errors(language_code: str) -> dict | None:
        try:
            file_path = DataProvider.config_path.joinpath(language_code, "errors.json")
            if not file_path.exists():
                return None
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            DataProvider.exception_handler(e)
            return None

    @staticmethod
    def get_ui_text(widget_tooltip: str, language_code: str) -> dict | None:
        try:
            file_path = DataProvider.config_path.joinpath(language_code, "ui_text.json")
            if not file_path.exists():
                return None
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file).get(widget_tooltip)
        except Exception as e:
            DataProvider.exception_handler(e)
            return None

    @staticmethod
    def get_supported_languages() -> str | None:
        try:
            if not DataProvider.config_path.exists():
                return None

            supported_languages = []
            for folder in DataProvider.config_path.iterdir():
                if folder.is_dir() and DataProvider.check_empty_dir(folder):
                    supported_languages.append(folder.name)

            dialog = ErrorDialogManager()
            return dialog.show_language_error_dialog(supported_languages)
        except Exception as e:
            DataProvider.exception_handler(e)
            return None

    @staticmethod
    def check_empty_dir(folder: pathlib.Path) -> bool | None:
        try:
            required_files = ["errors.json", "language_info.json", "tooltips.json", "ui_text.json"]
            for file_name in required_files:
                file_path = folder.joinpath(file_name)
                if not file_path.exists() or file_path.stat().st_size == 0:
                    return False
            return True
        except Exception as e:
            DataProvider.exception_handler(e)
            return None

    @staticmethod
    def exception_handler(exception: Exception) -> None:
        logger = setup_logger()
        logger.error("An error occurred: %s", exception, exc_info=True)
        ErrorDialogManager.show_simple_error_messagebox(exception)
