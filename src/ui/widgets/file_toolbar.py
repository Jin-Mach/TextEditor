import json
import pathlib

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QToolBar, QWidget, QPushButton, QHBoxLayout, QLabel, QLineEdit


class FileToolbar(QToolBar):
    tooltips_path = pathlib.Path(__file__).parent.parent.parent.joinpath("config", "tooltips", "tooltips_en.json")
    icons_path = pathlib.Path(__file__).parent.parent.parent.joinpath("icons", "file_icons")

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("fileToolbar")
        self.setAllowedAreas(Qt.ToolBarArea.TopToolBarArea)
        self.setOrientation(Qt.Orientation.Horizontal)
        self.setFloatable(False)
        self.setMovable(False)
        self.tooltips = self.load_tooltips(str(self.tooltips_path))
        self.addWidget(self.create_file_widget())
        self.addSeparator()
        self.addWidget(self.create_export_widget())
        self.addSeparator()
        self.addWidget(self.create_print_widget())
        self.addSeparator()
        self.addWidget(self.create_search_widget())

    def create_file_widget(self) -> QWidget:
        file_widget = QWidget()
        file_layout = QHBoxLayout()
        new_file_button = QPushButton()
        self.set_icon(new_file_button, "new_file_icon.png")
        self.set_tooltips(new_file_button, "new_file")
        open_file_button = QPushButton()
        self.set_icon(open_file_button, "open_file_icon.png")
        self.set_tooltips(open_file_button, "open_file")
        save_as_button = QPushButton()
        self.set_icon(save_as_button, "save_as_icon.png")
        self.set_tooltips(save_as_button, "save_as_file")
        self.save_button = QPushButton()
        self.save_button.setDisabled(True)
        self.set_icon(self.save_button, "save_icon.png")
        self.set_tooltips(self.save_button, "save_file")
        file_layout.addWidget(new_file_button)
        file_layout.addWidget(open_file_button)
        file_layout.addWidget(save_as_button)
        file_layout.addWidget(self.save_button)
        file_widget.setLayout(file_layout)
        return file_widget

    def create_export_widget(self) -> QWidget:
        export_widget = QWidget()
        export_layout = QHBoxLayout()
        save_as_html_button = QPushButton()
        self.set_icon(save_as_html_button, "save_as_html_icon.png")
        self.set_tooltips(save_as_html_button, "save_as_html")
        export_pdf_button = QPushButton()
        self.set_icon(export_pdf_button, "export_pdf_icon.png")
        self.set_tooltips(export_pdf_button, "export_to_pdf")
        export_layout.addWidget(save_as_html_button)
        export_layout.addWidget(export_pdf_button)
        export_widget.setLayout(export_layout)
        return export_widget

    def create_print_widget(self) -> QWidget:
        print_widget = QWidget()
        print_layout = QHBoxLayout()
        print_preview_button = QPushButton()
        self.set_icon(print_preview_button, "print_preview_icon.png")
        self.set_tooltips(print_preview_button, "print_preview")
        print_button = QPushButton()
        self.set_icon(print_button, "print_icon.png")
        self.set_tooltips(print_button, "print_document")
        print_layout.addWidget(print_preview_button)
        print_layout.addWidget(print_button)
        print_widget.setLayout(print_layout)
        return print_widget

    def create_search_widget(self) -> QWidget:
        search_widget = QWidget()
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("for search write here...")
        search_button = QPushButton()
        self.set_icon(search_button, "search_icon.png")
        self.set_tooltips(search_button, "search")
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        search_layout.addStretch()
        search_widget.setLayout(search_layout)
        return search_widget

    def set_icon(self, widget: QPushButton, icon_name: str) -> None:
        widget.setIcon(QIcon(str(self.icons_path.joinpath(icon_name))))
        widget.setIconSize(QSize(20, 20))

    @staticmethod
    def load_tooltips(tooltips_path: str) -> dict:
        with open(str(tooltips_path), "r", encoding="utf-8") as file:
            tooltips = json.load(file)
            return tooltips["file_tooltips"]

    def set_tooltips(self, widget: QWidget, tooltip_key: str) -> None:
        tooltip_text = self.tooltips.get(tooltip_key)
        widget.setToolTip(tooltip_text)
        widget.setToolTipDuration(5000)