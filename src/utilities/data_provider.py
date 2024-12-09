import json
import pathlib

from PyQt6.QtCore import QLocale


class DataProvider:

    @staticmethod
    def get_language_code() -> str:
        language = QLocale.system().name()
        language_directory = pathlib.Path(__file__).parent.parent.joinpath("config")
        language_folders = []
        for folder in language_directory.iterdir():
            if folder.is_dir():
                language_folders.append(folder.name)
        if language not in language_folders:
                language = "en_GB"
        return language

    @staticmethod
    def get_tooltips(widget_tooltip: str, language_code: str) -> dict:
        with open(str(pathlib.Path(__file__).parent.parent.joinpath("config", language_code, "tooltips.json")), "r", encoding="utf-8") as file:
            tooltips = json.load(file)[widget_tooltip]
            return tooltips

    @staticmethod
    def get_icons(icons_path: pathlib.Path) -> dict:
        icons_dict = {}
        for icon in icons_path.iterdir():
            if icon.is_file() and icon.suffix == ".png":
                key = icon.stem
                icons_dict[key] = icon
        return icons_dict

    @staticmethod
    def get_errors(language_code: str) -> dict:
        with open(str(pathlib.Path(__file__).parent.parent.joinpath("config", language_code, "errors.json")), "r", encoding="utf-8") as file:
            errors = json.load(file)
            return errors

    @staticmethod
    def get_ui_text(widget_tooltip: str, language_code: str) -> dict:
        with open(str(pathlib.Path(__file__).parent.parent.joinpath("config", language_code, "ui_text.json")), "r", encoding="utf-8") as file:
            ui_text = json.load(file)[widget_tooltip]
            return ui_text