import pathlib

from PyQt6.QtWidgets import QTextEdit

from src.utilities.logging_manager import setup_logger
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
                result = self.messagebox_manager.empty_text_error()
                if result == "dontSave":
                    self.text_edit.reset_text_edit()
                elif result == "save_as":
                    print("save_as")
                elif result == "cancel":
                    self.text_edit.setFocus()
            else:
                self.text_edit.reset_text_edit()
        except Exception as e:
            setup_logger().error(str(e))
            self.messagebox_manager.show_error_message(e)

    def open_file(self) -> None:
        try:
            if self.text_edit.toPlainText():
                result = self.messagebox_manager.empty_text_error()
                if result == "dontSave":
                    selected_file = str(self.dialog_manager.open_file_dialog())
                    self.load_file_content(selected_file)
                elif result == "save_as":
                    print("save_as")
                elif result == "cancel":
                    self.text_edit.setFocus()
            else:
                selected_file = self.dialog_manager.open_file_dialog()
                self.load_file_content(selected_file)
        except Exception as e:
            setup_logger().error(str(e))
            self.messagebox_manager.show_error_message(e)

    def load_file_content(self, file_path:str) -> None:
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
            setup_logger().error(str(e))
            self.messagebox_manager.show_error_message(e)