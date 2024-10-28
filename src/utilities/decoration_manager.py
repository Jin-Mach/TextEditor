import json
import pathlib


class DecorationManager:

    @staticmethod
    def get_tooltips(widget_tooltip: str) -> dict:
        with open(str(pathlib.Path(__file__).parent.parent.joinpath("config", "tooltips", "tooltips_en.json")), "r", encoding="utf-8") as file:
          tooltips = json.load(file)[widget_tooltip]
          return tooltips

    @staticmethod
    def get_icons(icons_path: pathlib.Path) -> dict:
        icons_dict = {}
        for icon in icons_path.iterdir():
            if icon.is_file() and icon.suffix == '.png':
                key = icon.stem
                icons_dict[key] = icon
        return icons_dict