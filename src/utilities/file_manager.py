from PyQt6.QtWidgets import QTextEdit

from src.utilities.logging_manager import setup_logger
from src.utilities.messagebox_manager import MessageboxManager


# noinspection PyUnresolvedReferences
class Filemanager:
    def __init__(self, text_edit: QTextEdit, parent=None) -> None:
        self.messagebox_manager = MessageboxManager()
        self.parent = parent
        self.text_edit = text_edit

    def new_file(self) -> None:
        try:
            if self.text_edit.toPlainText().strip():
                message = self.messagebox_manager
                result = message.empty_text_error(self.parent)
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
            print(e)