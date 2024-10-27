import json
import pathlib

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QColor, QPixmap, QFont
from PyQt6.QtWidgets import QToolBar, QWidget, QHBoxLayout, QComboBox, QPushButton


class TextToolbar(QToolBar):
    tooltips_path = pathlib.Path(__file__).parent.parent.parent.joinpath("config", "tooltips", "tooltips_en.json")
    icons_path = pathlib.Path(__file__).parent.parent.parent.joinpath("icons", "text_icons")
    font_list = ["Arial", "Calibri", "Comic Sans MS", "Courier New", "Georgia", "Helvetica", "Palatino", "Tahoma", "Times New Roman", "Verdana"]
    font_sizes = [8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
    combobox_colors = ["#000000", "#FFFFFF", "#1E90FF", "#32CD32", "#FF4500", "#FFA500", "#FFFF00", "#9370DB", "#8B4513", "#B22222"]

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("textToolbar")
        self.setAllowedAreas(Qt.ToolBarArea.TopToolBarArea)
        self.setOrientation(Qt.Orientation.Horizontal)
        self.setFloatable(False)
        self.setMovable(False)
        self.tooltips = self.load_tooltips(str(self.tooltips_path))
        self.addWidget(self.create_font_widget())
        self.addSeparator()
        self.addWidget(self.create_style_widget())
        self.addSeparator()
        self.addWidget(self.create_action_widget())
        self.addSeparator()
        self.addWidget(self.create_alignment_widget())
        self.addSeparator()
        self.addWidget(self.create_colors_widget())

    def create_font_widget(self) -> QWidget:
        font_widget = QWidget()
        font_layout = QHBoxLayout()
        self.font_family_combobox = QComboBox()
        self.font_family_combobox.setObjectName("fontFamily")
        for font in self.font_list:
            self.font_family_combobox.addItem(font)
            index = self.font_family_combobox.count() - 1
            self.font_family_combobox.setItemData(index, QFont(font), role=Qt.ItemDataRole.FontRole)
        self.set_tooltips(self.font_family_combobox, "font")
        self.font_size_combobox = QComboBox()
        self.font_size_combobox.setObjectName("fontSize")
        for size in self.font_sizes:
            self.font_size_combobox.addItem(str(size))
        self.font_size_combobox.setCurrentText("14")
        self.set_tooltips(self.font_size_combobox, "font_size")
        font_layout.addWidget(self.font_family_combobox)
        font_layout.addWidget(self.font_size_combobox)
        font_widget.setLayout(font_layout)
        return font_widget

    def create_style_widget(self) -> QWidget:
        style_widget = QWidget()
        style_layout = QHBoxLayout()
        bold_text_button = QPushButton()
        self.set_icons(bold_text_button, "bold_icon.png")
        self.set_tooltips(bold_text_button, "bold_text")
        italic_text_button = QPushButton()
        self.set_icons(italic_text_button, "italic_icon.png")
        self.set_tooltips(italic_text_button, "italic_text")
        underline_text_button = QPushButton()
        self.set_icons(underline_text_button, "underline_icon.png")
        self.set_tooltips(underline_text_button, "underline_text")
        strikethrough_text_button = QPushButton()
        self.set_icons(strikethrough_text_button, "strikethrough_icon.png")
        self.set_tooltips(strikethrough_text_button, "strikethrough_text")
        style_layout.addWidget(bold_text_button)
        style_layout.addWidget(italic_text_button)
        style_layout.addWidget(underline_text_button)
        style_layout.addWidget(strikethrough_text_button)
        style_widget.setLayout(style_layout)
        return style_widget

    def create_action_widget(self) -> QWidget:
        action_widget = QWidget()
        action_layout = QHBoxLayout()
        self.undo_button = QPushButton()
        self.set_icons(self.undo_button, "undo_icon.png")
        self.set_tooltips(self.undo_button, "undo")
        self.redo_button = QPushButton()
        self.set_icons(self.redo_button, "redo_icon.png")
        self.set_tooltips(self.redo_button, "redo")
        self.cut_button = QPushButton()
        select_all_button = QPushButton()
        self.set_icons(self.cut_button, "cut_icon.png")
        self.set_tooltips(self.cut_button, "cut")
        self.copy_button = QPushButton()
        self.set_icons(self.copy_button, "copy_icon.png")
        self.set_tooltips(self.copy_button, "copy")
        self.paste_button = QPushButton()
        self.set_icons(self.paste_button, "paste_icon.png")
        self.set_tooltips(self.paste_button, "paste")
        self.set_icons(select_all_button, "select_icon.png")
        self.set_tooltips(select_all_button, "select_all")
        delete_text_button = QPushButton()
        self.set_icons(delete_text_button, "delete_icon")
        self.set_tooltips(delete_text_button, "delete_text")
        action_layout.addWidget(self.undo_button)
        action_layout.addWidget(self.redo_button)
        action_layout.addWidget(self.cut_button)
        action_layout.addWidget(self.copy_button)
        action_layout.addWidget(self.paste_button)
        action_layout.addWidget(select_all_button)
        action_layout.addWidget(delete_text_button)
        action_widget.setLayout(action_layout)
        return action_widget

    def create_alignment_widget(self) -> QWidget:
        align_widget = QWidget()
        align_layout = QHBoxLayout()
        align_left_button = QPushButton()
        self.set_icons(align_left_button, "align_left_icon.png")
        self.set_tooltips(align_left_button, "align_left")
        align_center_button = QPushButton()
        self.set_icons(align_center_button, "align_center_icon.png")
        self.set_tooltips(align_center_button, "align_center")
        align_right_button = QPushButton()
        self.set_icons(align_right_button, "align_right_icon.png")
        self.set_tooltips(align_right_button, "align_right")
        align_justified_button = QPushButton()
        self.set_icons(align_justified_button, "align_justify_icon.png")
        self.set_tooltips(align_justified_button, "align_justified")
        align_layout.addWidget(align_left_button)
        align_layout.addWidget(align_center_button)
        align_layout.addWidget(align_right_button)
        align_layout.addWidget(align_justified_button)
        align_widget.setLayout(align_layout)
        return align_widget

    def create_colors_widget(self) -> QWidget:
        colors_widget = QWidget()
        colors_layout = QHBoxLayout()
        self.text_color_combobox = QComboBox()
        self.text_color_combobox.setObjectName("textColor")
        for color in self.combobox_colors:
            icon = self.create_color_icon(color)
            self.text_color_combobox.addItem(icon, "")
        default_color = "#000000"
        default_index = self.combobox_colors.index(default_color)
        self.text_color_combobox.setCurrentIndex(default_index)
        self.set_tooltips(self.text_color_combobox, "text_color")
        self.background_color_combobox = QComboBox()
        self.background_color_combobox.setObjectName("backgroundColor")
        for color in self.combobox_colors:
            icon = self.create_color_icon(color)
            self.background_color_combobox.addItem(icon, "")
        default_color = "#FFFFFF"
        default_index = self.combobox_colors.index(default_color)
        self.background_color_combobox.setCurrentIndex(default_index)
        self.set_tooltips(self.background_color_combobox, "background_color")
        colors_layout.addWidget(self.text_color_combobox)
        colors_layout.addWidget(self.background_color_combobox)
        colors_widget.setLayout(colors_layout)
        return colors_widget

    def set_icons(self, widget: QPushButton, icon_name: str) -> None:
        widget.setIcon(QIcon(str(self.icons_path.joinpath(str(icon_name)))))
        widget.setIconSize(QSize(20, 20))

    @staticmethod
    def load_tooltips(tooltips_path: str) -> dict:
        with open(tooltips_path, "r", encoding="utf-8") as file:
            tooltips = json.load(file)
            return tooltips["text_tooltips"]

    def set_tooltips(self, widget: QWidget, tooltip_key: str) -> None:
        tooltip_text = self.tooltips.get(tooltip_key)
        widget.setToolTip(tooltip_text)
        widget.setToolTipDuration(5000)

    def create_color_icon(self, color_hex):
        pixmap = QPixmap(30, 30)
        pixmap.fill(QColor(color_hex))
        return QIcon(pixmap)