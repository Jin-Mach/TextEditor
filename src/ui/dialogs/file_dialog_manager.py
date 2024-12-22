import pathlib
from typing import Optional

from PyQt6.QtWidgets import QFileDialog

from src.utilities.data_provider import DataProvider
from src.utilities.exception_manager import ExceptionManager
from src.ui.dialogs.messagebox_manager import MessageboxManager


# noinspection PyUnresolvedReferences
class FileDialogManager:
    def __init__(self, parent=None) -> None:
        self.parent = parent
        language_code = self.parent.language_code
        self.messagebox_manager = MessageboxManager(self.parent)
        self.dialog_path = pathlib.Path(__file__).resolve().anchor
        self.ui_text = DataProvider.get_ui_text("dialog", language_code)

    def open_file_dialog(self) -> Optional[str]:
        try:
            file_name, _ = QFileDialog.getOpenFileName(self.parent, self.ui_text.get("newfileTitle"), str(self.dialog_path),
                                                       self.ui_text.get("fileFilter"))
            if file_name:
                return file_name
            return None
        except Exception as e:
            ExceptionManager.exception_handler(e)

    def save_document_dialog(self, file_type: str) -> Optional[str]:
        try:
            file_name, _ = QFileDialog.getSaveFileName(self.parent, self.ui_text.get("savedocumentTitle"),
                                                       str(self.dialog_path), file_type)
            if file_name:
                return file_name
            return None
        except Exception as e:
            ExceptionManager.exception_handler(e)