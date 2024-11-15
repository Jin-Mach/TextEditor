import pathlib

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QColor, QPixmap, QFont
from PyQt6.QtWidgets import QToolBar, QWidget, QHBoxLayout, QComboBox, QPushButton

from src.ui.widgets.text_edit import TextEdit
from src.utilities.data_provider import DataProvider
from src.utilities.text_manager import TextManager


# noinspection PyUnresolvedReferences
class TextToolbar(QToolBar):
    font_list = ["Arial", "Calibri", "Comic Sans MS", "Courier New", "Georgia", "Helvetica", "Palatino", "Tahoma", "Times New Roman", "Verdana"]
    font_sizes = [8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
    combobox_colors = ["#000000", "#FFFFFF", "#1E90FF", "#32CD32", "#FF4500", "#FFA500", "#FFFF00", "#9370DB", "#8B4513", "#B22222"]

    def __init__(self, text_edit: TextEdit, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("textToolbar")
        self.text_edit = text_edit
        self.text_manager = TextManager(self.text_edit, self)
        self.setAllowedAreas(Qt.ToolBarArea.TopToolBarArea)
        self.setOrientation(Qt.Orientation.Horizontal)
        self.setFloatable(False)
        self.setMovable(False)
        self.create_main_gui()
        self.set_icons()
        self.set_tooltips()
        self.create_connection()

    def create_main_gui(self) -> None:
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
        self.font_size_combobox = QComboBox()
        self.font_size_combobox.setObjectName("fontSize")
        for size in self.font_sizes:
            self.font_size_combobox.addItem(str(size))
        self.font_size_combobox.setCurrentText("14")
        font_layout.addWidget(self.font_family_combobox)
        font_layout.addWidget(self.font_size_combobox)
        font_widget.setLayout(font_layout)
        return font_widget

    def create_style_widget(self) -> QWidget:
        style_widget = QWidget()
        style_layout = QHBoxLayout()
        self.bold_text_button = QPushButton()
        self.bold_text_button.setObjectName("bold")
        self.italic_text_button = QPushButton()
        self.italic_text_button.setObjectName("italic")
        self.underline_text_button = QPushButton()
        self.underline_text_button.setObjectName("underline")
        self.strikethrough_text_button = QPushButton()
        self.strikethrough_text_button.setObjectName("strikethrough")
        style_layout.addWidget(self.bold_text_button)
        style_layout.addWidget(self.italic_text_button)
        style_layout.addWidget(self.underline_text_button)
        style_layout.addWidget(self.strikethrough_text_button)
        style_widget.setLayout(style_layout)
        return style_widget

    def create_action_widget(self) -> QWidget:
        action_widget = QWidget()
        action_layout = QHBoxLayout()
        self.undo_button = QPushButton()
        self.undo_button.setObjectName("undo")
        self.redo_button = QPushButton()
        self.redo_button.setObjectName("redo")
        self.cut_button = QPushButton()
        self.cut_button.setObjectName("cut")
        self.copy_button = QPushButton()
        self.copy_button.setObjectName("copy")
        self.paste_button = QPushButton()
        self.paste_button.setObjectName("paste")
        self.select_all_button = QPushButton()
        self.select_all_button.setObjectName("selectAll")
        self.delete_text_button = QPushButton()
        self.delete_text_button.setObjectName("deleteText")
        action_layout.addWidget(self.undo_button)
        action_layout.addWidget(self.redo_button)
        action_layout.addWidget(self.cut_button)
        action_layout.addWidget(self.copy_button)
        action_layout.addWidget(self.paste_button)
        action_layout.addWidget(self.select_all_button)
        action_layout.addWidget(self.delete_text_button)
        action_widget.setLayout(action_layout)
        return action_widget

    def create_alignment_widget(self) -> QWidget:
        align_widget = QWidget()
        align_layout = QHBoxLayout()
        self.align_left_button = QPushButton()
        self.align_left_button.setObjectName("alignLeft")
        self.align_center_button = QPushButton()
        self.align_center_button.setObjectName("alignCenter")
        self.align_right_button = QPushButton()
        self.align_right_button.setObjectName("alignRight")
        self.align_justified_button = QPushButton()
        self.align_justified_button.setObjectName("alignJustified")
        align_layout.addWidget(self.align_left_button)
        align_layout.addWidget(self.align_center_button)
        align_layout.addWidget(self.align_right_button)
        align_layout.addWidget(self.align_justified_button)
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
        self.background_color_combobox = QComboBox()
        self.background_color_combobox.setObjectName("backgroundColor")
        for color in self.combobox_colors:
            icon = self.create_color_icon(color)
            self.background_color_combobox.addItem(icon, "")
        default_color = "#FFFFFF"
        default_index = self.combobox_colors.index(default_color)
        self.background_color_combobox.setCurrentIndex(default_index)
        colors_layout.addWidget(self.text_color_combobox)
        colors_layout.addWidget(self.background_color_combobox)
        colors_widget.setLayout(colors_layout)
        return colors_widget

    def set_icons(self) -> None:
        icons_dict = DataProvider.get_icons(pathlib.Path(__file__).parent.parent.parent.joinpath("icons", "text_icons"))
        buttons = self.findChildren(QPushButton)
        for button in buttons:
            name = button.objectName()
            if name in icons_dict.keys():
                button.setIcon(QIcon(str(icons_dict[name])))
                button.setIconSize(QSize(25, 25))

    def set_tooltips(self) -> None:
        tooltips = DataProvider.get_tooltips("textTooltips")
        for button in self.findChildren(QPushButton):
            if button.objectName() in tooltips:
                tooltips_text = tooltips.get(button.objectName())
                button.setToolTip(tooltips_text)
                button.setToolTipDuration(5000)
        for combobox in self.findChildren(QComboBox):
            if combobox.objectName() in tooltips:
                tooltips_text = tooltips.get(combobox.objectName())
                combobox.setToolTip(tooltips_text)
                combobox.setToolTipDuration(5000)

    @staticmethod
    def create_color_icon(color_hex):
        pixmap = QPixmap(30, 30)
        pixmap.fill(QColor(color_hex))
        return QIcon(pixmap)

    def create_connection(self) -> None:
        self.font_family_combobox.currentIndexChanged.connect(self.text_manager.set_font_style)
        self.font_size_combobox.currentIndexChanged.connect(self.text_manager.set_font_style)
        self.bold_text_button.clicked.connect(lambda: self.text_manager.set_text_format("bold"))
        self.italic_text_button.clicked.connect(lambda: self.text_manager.set_text_format("italic"))
        self.underline_text_button.clicked.connect(lambda: self.text_manager.set_text_format("underline"))
        self.strikethrough_text_button.clicked.connect(lambda: self.text_manager.set_text_format("strikeout"))

    def reset_text_toolbar(self) -> None:
        self.font_family_combobox.setCurrentText("Arial")
        self.font_size_combobox.setCurrentText("14")