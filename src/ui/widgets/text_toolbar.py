import pathlib

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QColor, QPixmap, QFont, QGuiApplication
from PyQt6.QtWidgets import QToolBar, QWidget, QHBoxLayout, QComboBox, QPushButton

from src.ui.widgets.text_edit import TextEdit
from src.utilities.data_provider import DataProvider
from src.utilities.text_manager import TextManager


# noinspection PyUnresolvedReferences
class TextToolbar(QToolBar):
    font_list = ["Arial", "Calibri", "Comic Sans MS", "Courier New", "Georgia", "Impact", "Tahoma", "Times New Roman", "Trebuchet MS", "Verdana"]
    font_sizes = [8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
    combobox_colors = ["#000000", "#ffffff", "#1e90ff", "#32cd32", "#ff4500", "#ffa500", "#ffff00", "#9370db", "#8b4513", "#b22222"]

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
        self.update_edit_buttons()
        self.text_edit.cursorPositionChanged.connect(self.update_edit_buttons)
        self.text_edit.selectionChanged.connect(self.update_format_buttons)

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
        self.bold_text_button.setCheckable(True)
        self.italic_text_button = QPushButton()
        self.italic_text_button.setObjectName("italic")
        self.italic_text_button.setCheckable(True)
        self.underline_text_button = QPushButton()
        self.underline_text_button.setObjectName("underline")
        self.underline_text_button.setCheckable(True)
        self.strikeout_text_button = QPushButton()
        self.strikeout_text_button.setObjectName("strikeout")
        self.strikeout_text_button.setCheckable(True)
        style_layout.addWidget(self.bold_text_button)
        style_layout.addWidget(self.italic_text_button)
        style_layout.addWidget(self.underline_text_button)
        style_layout.addWidget(self.strikeout_text_button)
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
        self.align_left_button.setCheckable(True)
        self.align_left_button.setEnabled(True)
        self.align_center_button = QPushButton()
        self.align_center_button.setObjectName("alignCenter")
        self.align_center_button.setCheckable(True)
        self.align_right_button = QPushButton()
        self.align_right_button.setObjectName("alignRight")
        self.align_right_button.setCheckable(True)
        self.align_justified_button = QPushButton()
        self.align_justified_button.setObjectName("alignJustify")
        self.align_justified_button.setCheckable(True)
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
        self.text_color_combobox.setFixedWidth(40)
        self.text_color_combobox.setFixedHeight(30)
        for color in self.combobox_colors:
            icon = self.create_color_icon(color)
            self.text_color_combobox.addItem(icon, color)
            self.text_color_combobox.setItemData(self.text_color_combobox.count() - 1, color)
        default_color = "#000000"
        default_index = self.combobox_colors.index(default_color)
        self.text_color_combobox.setCurrentIndex(default_index)
        self.background_color_combobox = QComboBox()
        self.background_color_combobox.setObjectName("backgroundColor")
        self.background_color_combobox.setFixedWidth(40)
        self.background_color_combobox.setFixedHeight(30)
        for color in self.combobox_colors:
            icon = self.create_color_icon(color)
            self.background_color_combobox.addItem(icon, color)
            self.background_color_combobox.setItemData(self.background_color_combobox.count() - 1, color)
        default_color = "#ffffff"
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
        self.strikeout_text_button.clicked.connect(lambda: self.text_manager.set_text_format("strikeout"))
        self.undo_button.clicked.connect(self.text_edit.undo)
        self.redo_button.clicked.connect(self.text_edit.redo)
        self.cut_button.clicked.connect(self.text_edit.cut)
        self.copy_button.clicked.connect(self.text_edit.copy)
        self.paste_button.clicked.connect(self.text_edit.paste)
        self.select_all_button.clicked.connect(self.text_edit.selectAll)
        self.delete_text_button.clicked.connect(self.text_manager.clear_text_edit)
        self.align_left_button.clicked.connect(lambda: self.text_manager.set_alignment(Qt.AlignmentFlag.AlignLeft))
        self.align_center_button.clicked.connect(lambda: self.text_manager.set_alignment(Qt.AlignmentFlag.AlignCenter))
        self.align_right_button.clicked.connect(lambda: self.text_manager.set_alignment(Qt.AlignmentFlag.AlignRight))
        self.align_justified_button.clicked.connect(lambda: self.text_manager.set_alignment(Qt.AlignmentFlag.AlignJustify))
        self.text_color_combobox.currentIndexChanged.connect(lambda: self.text_manager.set_text_and_background_color(self.text_color_combobox))
        self.background_color_combobox.currentIndexChanged.connect(lambda: self.text_manager.set_text_and_background_color(self.background_color_combobox))

    def reset_text_toolbar(self) -> None:
        buttons = [self.bold_text_button, self.italic_text_button, self.underline_text_button, self.strikeout_text_button,
                   self.align_left_button, self.align_center_button, self.align_right_button, self.align_justified_button]
        self.font_family_combobox.setCurrentIndex(self.font_family_combobox.findText("Arial"))
        self.font_size_combobox.setCurrentIndex(self.font_size_combobox.findText("14"))
        for button in buttons:
            button.setChecked(False)
        self.text_color_combobox.setCurrentIndex(self.text_color_combobox.findText("#000000"))
        self.background_color_combobox.setCurrentIndex(self.background_color_combobox.findText("#ffffff"))

    def update_edit_buttons(self) -> None:
        self.bold_text_button.setEnabled(self.text_edit.textCursor().hasSelection())
        self.italic_text_button.setEnabled(self.text_edit.textCursor().hasSelection())
        self.underline_text_button.setEnabled(self.text_edit.textCursor().hasSelection())
        self.strikeout_text_button.setEnabled(self.text_edit.textCursor().hasSelection())
        self.undo_button.setEnabled(self.text_edit.document().isUndoAvailable())
        self.redo_button.setEnabled(self.text_edit.document().isRedoAvailable())
        self.cut_button.setEnabled(self.text_edit.textCursor().hasSelection())
        self.copy_button.setEnabled(self.text_edit.textCursor().hasSelection())
        self.paste_button.setEnabled(bool(QGuiApplication.clipboard().text()))
        self.select_all_button.setEnabled(bool(self.text_edit.toPlainText()))
        self.delete_text_button.setEnabled(bool(self.text_edit.toPlainText()))
        self.align_left_button.setEnabled(self.text_edit.textCursor().hasSelection())
        self.align_center_button.setEnabled(self.text_edit.textCursor().hasSelection())
        self.align_right_button.setEnabled(self.text_edit.textCursor().hasSelection())
        self.align_justified_button.setEnabled(self.text_edit.textCursor().hasSelection())

    def update_format_buttons(self) -> None:
        text_format = self.get_text_format()
        alignment_buttons = [self.align_left_button, self.align_center_button, self.align_right_button, self.align_justified_button]
        for alignmentbutton in alignment_buttons:
            alignmentbutton.setChecked(False)
        widgets = [self.font_family_combobox, self.font_size_combobox, self.bold_text_button, self.italic_text_button,
                   self.underline_text_button, self.strikeout_text_button, self.findChild(QPushButton, text_format[6]),
                   self.text_color_combobox, self.background_color_combobox]
        alignment_button = widgets[-3]
        self.block_signals(widgets)
        self.font_family_combobox.setCurrentText(text_format[0])
        self.font_size_combobox.setCurrentText(text_format[1])
        self.bold_text_button.setChecked(text_format[2])
        self.italic_text_button.setChecked(text_format[3])
        self.underline_text_button.setChecked(text_format[4])
        self.strikeout_text_button.setChecked(text_format[5])
        alignment_button.setChecked(True)
        text_color_index = self.text_color_combobox.findData(text_format[-2])
        background_color_index = self.background_color_combobox.findData(text_format[-1])
        if text_color_index != -1:
            self.text_color_combobox.setCurrentIndex(text_color_index)
        if background_color_index != -1:
            self.background_color_combobox.setCurrentIndex(background_color_index)
        self.activate_signals(widgets)

    def get_text_format(self) -> tuple:
        cursor = self.text_edit.textCursor()
        char_format = cursor.charFormat()
        alignment = self.text_edit.alignment()
        alignment_name = "alignLeft"
        if cursor and char_format.isValid():
            font = char_format.font()
            font_family = font.family()
            if not font_family:
                font_family = "Arial"
            font_size = font.pointSize()
            if not font_size:
                font_size = 14
            is_bold = font.bold()
            is_italic = font.italic()
            is_underline = font.underline()
            is_strikeout = font.strikeOut()
            if alignment:
                alignment_name = alignment.name[0].lower() + alignment.name[1:]
            text_color = char_format.foreground().color().name()
            background_color = char_format.background().color().name()
            if background_color == "#000000":
                background_color = "#ffffff"
            return str(font_family), str(font_size), is_bold, is_italic, is_underline, is_strikeout, alignment_name, text_color, background_color
        return "Arial", "14", False, False, False, False, "alignLeft", "#000000", "#ffffff"

    @staticmethod
    def block_signals(widgets: list) -> None:
        for widget in widgets:
            widget.blockSignals(True)

    @staticmethod
    def activate_signals(widgets: list) -> None:
        for widget in widgets:
            widget.blockSignals(False)