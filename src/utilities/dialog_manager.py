import pathlib

from PyQt6.QtWidgets import QFileDialog

from src.utilities.data_provider import DataProvider
from src.utilities.logging_manager import setup_logger
from src.utilities.messagebox_manager import MessageboxManager


# noinspection PyUnresolvedReferences
class DialogManager:
    def __init__(self, parent=None) -> None:
        self.parent = parent
        self.messagebox_manager = MessageboxManager(self.parent)
        self.dialog_path = pathlib.Path(__file__).resolve().anchor
        self.ui_text = DataProvider.get_ui_text("dialog")

    def open_file_dialog(self) -> str:
        try:
            file_name, _ = QFileDialog.getOpenFileName(self.parent, self.ui_text.get("newfileTitle"), str(self.dialog_path),
                                                       self.ui_text.get("fileFilter"))
            if file_name:
                return file_name
        except Exception as e:
            setup_logger().error(str(e))
            self.messagebox_manager.show_error_message(e)