from PyQt6.QtWidgets import QStatusBar, QLabel

from src.utilities.data_provider import DataProvider


class StatusBar(QStatusBar):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("statusBar")
        self.create_gui()
        self.set_text_labels()

    def create_gui(self) -> None:
        self.character_count_label = QLabel()
        self.line_count_label = QLabel()
        self.cursor_position_label = QLabel()
        self.document_format = QLabel("utf-8")
        self.addWidget(self.character_count_label)
        self.addWidget(self.line_count_label)
        self.addWidget(self.cursor_position_label)
        self.addPermanentWidget(self.document_format)

    def set_text_labels(self) -> None:
        ui_text = DataProvider.get_ui_text("statusbar")
        self.character_count_label.setText(ui_text.get("characters"))
        self.line_count_label.setText(ui_text.get("lines"))
        self.cursor_position_label.setText(ui_text.get("cursor"))

    def update_count_labels(self, characters_count: int, lines_count: int, cursor_line: int, cursor_char: int) -> None:
        self.character_count_label.setText(f"Characters: {characters_count}")
        self.line_count_label.setText(f"Lines: {lines_count}")
        self.cursor_position_label.setText(f"Cursor: Line: {cursor_line}, Char: {cursor_char}")