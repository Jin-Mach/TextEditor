from PyQt6.QtGui import QFont, QTextCharFormat, QColor
from PyQt6.QtWidgets import QComboBox

from src.ui.widgets.text_edit import TextEdit
from src.utilities.exception_manager import ExceptionManager


class TextManager:
    def __init__(self, text_edit: TextEdit, parent=None) -> None:
        self.parent = parent
        self.text_edit = text_edit

    def check_selection(self) -> bool:
        cursor = self.text_edit.textCursor()
        return cursor.hasSelection()

    def set_font_style(self) -> None:
        try:
            font_combobox_text = self.parent.findChild(QComboBox, "fontFamily").currentText()
            size_combobox_text = self.parent.findChild(QComboBox, "fontSize").currentText()
            char_format = QTextCharFormat()
            if self.check_selection():
                char_format.setFont(QFont(str(font_combobox_text), int(size_combobox_text)))
                self.text_edit.textCursor().mergeCharFormat(char_format)
            else:
                cursor = self.text_edit.textCursor()
                char_format.setFont(QFont(str(font_combobox_text), int(size_combobox_text)))
                cursor.mergeCharFormat(char_format)
                self.text_edit.setTextCursor(cursor)
            self.text_edit.setFocus()
        except Exception as e:
            ExceptionManager.exception_handler(e)

    def set_text_format(self, text_format: str) -> None:
        try:
            char_format = QTextCharFormat()
            is_bold, is_italic, is_underline, is_strikeout = self.text_edit.get_text_format()
            if self.check_selection():
                if text_format == "bold":
                    if is_bold:
                        char_format.setFontWeight(QFont.Weight.Normal)
                    else:
                        char_format.setFontWeight(QFont.Weight.Bold)
                elif text_format == "italic":
                    if is_italic:
                        char_format.setFontItalic(False)
                    else:
                        char_format.setFontItalic(True)
                elif text_format == "underline":
                    if is_underline:
                        char_format.setFontUnderline(False)
                    else:
                        char_format.setFontUnderline(True)
                elif text_format == "strikeout":
                    if is_strikeout:
                        char_format.setFontStrikeOut(False)
                    else:
                        char_format.setFontStrikeOut(True)
                self.text_edit.textCursor().mergeCharFormat(char_format)
        except Exception as e:
            ExceptionManager.exception_handler(e)

    def set_text_and_background_color(self, combobox: QComboBox) -> None:
        try:
            index = combobox.currentIndex()
            color = combobox.itemData(index)
            char_format = QTextCharFormat()
            if self.check_selection():
                if combobox.objectName() == "textColor":
                    char_format.setForeground(QColor(color))
                elif combobox.objectName() == "backgroundColor":
                    char_format.setBackground(QColor(color))
                self.text_edit.textCursor().mergeCharFormat(char_format)
            else:
                cursor = self.text_edit.textCursor()
                if combobox.objectName() == "textColor":
                    char_format.setForeground(QColor(color))
                elif combobox.objectName() == "backgroundColor":
                    char_format.setBackground(QColor(color))
                cursor.mergeCharFormat(char_format)
                self.text_edit.setTextCursor(cursor)
            self.text_edit.setFocus()
        except Exception as e:
            ExceptionManager.exception_handler(e)