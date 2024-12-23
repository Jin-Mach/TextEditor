from PyQt6.QtGui import QTextCursor, QTextCharFormat,  QColor
from PyQt6.QtWidgets import QTextEdit, QLineEdit

from src.utilities.data_provider import DataProvider
from src.utilities.exception_manager import ExceptionManager
from src.ui.dialogs.messagebox_manager import MessageboxManager

# noinspection PyUnresolvedReferences
class FindManager:
    def __init__(self, languague_code: str, search_input: QLineEdit, text_edit: QTextEdit, parent=None) -> None:
        self.parent = parent
        self.language_code = languague_code
        self.search_input = search_input
        self.text_edit = text_edit
        self.ui_text = DataProvider.get_ui_text("messagebox", self.language_code)

    def find_text(self) -> None:
        try:
            search_text = self.search_input.text().strip()
            if not search_text:
                messagebox_manager = MessageboxManager(self.parent)
                messagebox_manager.show_empty_document_message(self.text_edit, self.ui_text.get("emptySearch"))
                self.search_input.setFocus()
                return
            elif not self.text_edit.toPlainText():
                messagebox_manager = MessageboxManager(self.parent)
                messagebox_manager.show_empty_document_message(self.text_edit, self.ui_text.get("emptytextSearch"))
                self.text_edit.setFocus()
                return
            else:
                cursor = self.text_edit.textCursor()
                cursor.movePosition(QTextCursor.MoveOperation.Start)
                self.text_edit.setTextCursor(cursor)
                extra_selections = []
                while self.text_edit.find(search_text):
                    char_format = QTextCharFormat()
                    char_format.setBackground(QColor("yellow"))
                    selection = QTextEdit.ExtraSelection()
                    selection.cursor = self.text_edit.textCursor()
                    selection.format = char_format
                    extra_selections.append(selection)
                self.text_edit.setExtraSelections(extra_selections)
                cursor.movePosition(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.MoveAnchor)
                self.text_edit.setTextCursor(cursor)
                if not extra_selections:
                    messagebox_manager = MessageboxManager(self.parent)
                    messagebox_manager.show_empty_document_message(self.text_edit, ui_text.get("notFound"))
                    self.search_input.setFocus()
                    return
        except Exception as e:
            ExceptionManager.exception_handler(e)