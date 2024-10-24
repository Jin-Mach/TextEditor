from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QToolBar, QWidget, QHBoxLayout, QComboBox, QPushButton


class TextToolbar(QToolBar):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("textToolbar")
        self.setAllowedAreas(Qt.ToolBarArea.TopToolBarArea)
        self.setOrientation(Qt.Orientation.Horizontal)
        self.setFloatable(False)
        self.setMovable(False)
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
        self.font_size_combobox = QComboBox()
        font_layout.addWidget(self.font_family_combobox)
        font_layout.addWidget(self.font_size_combobox)
        font_widget.setLayout(font_layout)
        return font_widget

    def create_style_widget(self) -> QWidget:
        style_widget = QWidget()
        style_layout = QHBoxLayout()
        bold_text_button = QPushButton()
        italic_text_button = QPushButton()
        underline_text_button = QPushButton()
        strikethrough_text_button = QPushButton()
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
        self.redo_button = QPushButton()
        self.copy_button = QPushButton()
        self.paste_button = QPushButton()
        self.cut_button = QPushButton()
        select_all_button = QPushButton()
        delete_all_button = QPushButton()
        action_layout.addWidget(self.undo_button)
        action_layout.addWidget(self.redo_button)
        action_layout.addWidget(self.copy_button)
        action_layout.addWidget(self.paste_button)
        action_layout.addWidget(self.cut_button)
        action_layout.addWidget(select_all_button)
        action_layout.addWidget(delete_all_button)
        action_widget.setLayout(action_layout)
        return action_widget

    def create_alignment_widget(self) -> QWidget:
        align_widget = QWidget()
        align_layout = QHBoxLayout()
        align_left_button = QPushButton()
        align_center_button = QPushButton()
        align_right_button = QPushButton()
        align_justified_button = QPushButton()
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
        self.background_color_combobox = QComboBox()
        colors_layout.addWidget(self.text_color_combobox)
        colors_layout.addWidget(self.background_color_combobox)
        colors_widget.setLayout(colors_layout)
        return colors_widget