import pathlib

from PyQt6.QtWidgets import QTextEdit

from src.utilities.exception_manager import ExceptionManager
from src.utilities.messagebox_manager import MessageboxManager
from src.utilities.dialog_manager import DialogManager


# noinspection PyUnresolvedReferences
class FileManager:
    def __init__(self, text_edit: QTextEdit, parent=None) -> None:
        self.parent = parent
        self.last_file_path = ""
        self.messagebox_manager = MessageboxManager(self.parent)
        self.dialog_manager = DialogManager(self.parent.parent)
        self.text_edit = text_edit

    def new_file(self) -> None:
        try:
            if self.text_edit.toPlainText().strip():
                result = self.messagebox_manager.show_save_question_message()
                if result == "dontSave":
                    self.text_edit.reset_text_edit()
                    self.last_file_path = ""
                elif result == "saveAs":
                    self.save_file_as()
                elif result == "cancel":
                    self.text_edit.setFocus()
            else:
                self.text_edit.reset_text_edit()
        except Exception as e:
            ExceptionManager.exception_handler(e)

    def open_file(self) -> None:
        try:
            if self.text_edit.toPlainText():
                result = self.messagebox_manager.show_save_question_message()
                if result == "dontSave":
                    selected_file = str(self.dialog_manager.open_file_dialog())
                    if selected_file != "":
                        self.load_file_content(selected_file)
                elif result == "saveAs":
                    self.save_file_as()
                elif result == "cancel":
                    self.text_edit.setFocus()
            else:
                selected_file = self.dialog_manager.open_file_dialog()
                self.load_file_content(selected_file)
        except Exception as e:
            ExceptionManager.exception_handler(e)

    def save_file_as(self) -> None:
        try:
            if not self.text_edit.toPlainText():
                self.messagebox_manager.show_empty_document_message()
            else:
                file_path = self.dialog_manager.save_document_dialog("Textové soubory (*.txt)")
                if file_path:
                    self.save_document(file_path, "txt")
                    self.last_file_path = file_path
                    self.parent.save_button.setDisabled(False)
                self.text_edit.setFocus()
        except Exception as e:
            ExceptionManager.exception_handler(e)

    def save_file(self) -> None:
        try:
            if not self.text_edit.toPlainText():
                self.messagebox_manager.show_empty_document_message()
            else:
                self.save_document(self.last_file_path, "txt")

        except Exception as e:
            ExceptionManager.exception_handler(e)

    def load_file_content(self, file_path: str) -> None:
        try:
            if not file_path or not pathlib.Path(file_path).exists():
                self.text_edit.setFocus()
                return
            if file_path.endswith(".html"):
                with open(file_path, "r", encoding="utf-8") as file:
                    self.text_edit.setHtml(file.read())
            elif file_path.endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as file:
                    self.text_edit.setPlainText(file.read())
            self.last_file_path = file_path
            self.parent.save_button.setDisabled(False)
            cursor = self.text_edit.textCursor()
            cursor.movePosition(cursor.MoveOperation.End)
            self.text_edit.setTextCursor(cursor)
            self.text_edit.setFocus()
        except Exception as e:
            ExceptionManager.exception_handler(e)

    def save_document(self, file_path: str, file_type: str) -> None:
        try:
            if file_type == "txt":
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.text_edit.toPlainText())
            elif file_type == "html":
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.text_edit.toHtml())
            self.text_edit.setFocus()
        except Exception as e:
            ExceptionManager.exception_handler(e)