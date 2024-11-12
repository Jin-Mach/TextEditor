from PyQt6.QtGui import QFont, QTextCharFormat
from PyQt6.QtWidgets import QTextEdit, QComboBox

from src.utilities.exception_manager import ExceptionManager


class TextManager:
    def __init__(self, text_edit: QTextEdit, parent=None) -> None:
        self.parent = parent
        self.text_edit = text_edit

    def check_selection(self) -> bool:
        cursor = self.text_edit.textCursor()
        if cursor.hasSelection():
            return True
        return False

    def set_font_style(self) -> None:
        try:
            font_combobox_text = self.parent.findChild(QComboBox, "fontFamily").currentText()
            size_combobox_text = self.parent.findChild(QComboBox, "fontSize").currentText()
            if self.check_selection():
                char_format = QTextCharFormat()
                char_format.setFont(QFont(str(font_combobox_text), int(size_combobox_text)))
                self.text_edit.textCursor().mergeCharFormat(char_format)
            else:
                self.text_edit.setFont(QFont(str(font_combobox_text), int(size_combobox_text)))
            self.text_edit.setFocus()
        except Exception as e:
            ExceptionManager.exception_handler(e)