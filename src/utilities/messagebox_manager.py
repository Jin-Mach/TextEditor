import pathlib
import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMessageBox, QApplication, QPushButton

from src.utilities.data_provider import DataProvider


class MessageboxManager:
    def __init__(self, parent=None):
        self.parent = parent
        self.ui_text = DataProvider.get_ui_text("messagebox")
        self.icons_path = pathlib.Path(__file__).parent.parent.joinpath("icons", "dialog_icons")

    def show_load_error_message(self, exception_error: Exception, style_file_path: str) -> None:
        message_box = QMessageBox()
        message_box.setWindowIcon(QIcon(str(self.icons_path.joinpath("loading.png"))))
        message_box.setWindowTitle(self.ui_text.get("loadingError"))
        message_box.setIcon(QMessageBox.Icon.Critical)
        message_box.setText(self.set_error_text(exception_error) + "\n" + style_file_path)
        self.dont_save_button = message_box.addButton(self.ui_text.get("applicationContinue"), QMessageBox.ButtonRole.AcceptRole)
        self.dont_save_button.setObjectName("applicationContinue")
        self.cancel_button = message_box.addButton(self.ui_text.get("applicationCancel"), QMessageBox.ButtonRole.RejectRole)
        self.cancel_button.setObjectName("applicationCancel")
        self.set_tooltips(message_box)
        message_box.exec()
        if message_box.clickedButton() == self.cancel_button:
            sys.exit(1)

    def show_error_message(self, exception_error: Exception) -> None:
        message_box = QMessageBox(self.parent)
        message_box.setWindowTitle(self.ui_text.get("errorMessage"))
        message_box.setWindowIcon(QIcon(str(self.icons_path.joinpath("error.png"))))
        message_box.setText(self.set_error_text(exception_error))
        self.copy_button = message_box.addButton(self.ui_text.get("errorCopy"), QMessageBox.ButtonRole.AcceptRole)
        self.copy_button.setObjectName("errorCopy")
        self.cancel_button = message_box.addButton(self.ui_text.get("errorCancel"), QMessageBox.ButtonRole.RejectRole)
        self.cancel_button.setObjectName("errorCancel")
        self.set_tooltips(message_box)
        message_box.exec()
        if message_box.clickedButton() == self.copy_button:
            QApplication.clipboard().setText(self.set_error_text(exception_error))
            message_box.close()

    def empty_text_error(self) -> str:
        message_box = QMessageBox(self.parent)
        message_box.setWindowTitle(self.ui_text.get("emptyTitle"))
        message_box.setText(self.ui_text.get("emptyText"))
        self.dont_save_button = QPushButton(self.ui_text.get("dontSave"))
        self.dont_save_button.setObjectName("dontSave")
        self.save_as_button = QPushButton(self.ui_text.get("saveAs"))
        self.save_as_button.setObjectName("saveAs")
        self.cancel_button = QPushButton(self.ui_text.get("cancel"))
        self.cancel_button.setObjectName("cancel")
        message_box.addButton(self.dont_save_button, QMessageBox.ButtonRole.ActionRole)
        message_box.addButton(self.save_as_button, QMessageBox.ButtonRole.ActionRole)
        message_box.addButton(self.cancel_button, QMessageBox.ButtonRole.RejectRole)
        message_box.setDefaultButton(self.cancel_button)
        self.set_tooltips(message_box)
        message_box.exec()
        if message_box.clickedButton() == self.dont_save_button:
            return "dontSave"
        elif message_box.clickedButton() == self.save_as_button:
            return "save_as"
        elif message_box.clickedButton() == self.cancel_button:
            return "cancel"

    @staticmethod
    def set_tooltips(parent) -> None:
        tooltips = DataProvider.get_tooltips("messageboxTooltips")
        for button in parent.findChildren(QPushButton):
            if button.objectName() in tooltips:
                tooltips_text = tooltips.get(button.objectName())
                button.setToolTip(tooltips_text)
                button.setToolTipDuration(5000)

    @staticmethod
    def set_error_text(exception_error: Exception) -> str:
        errors = DataProvider.get_errors()
        if isinstance(exception_error, FileNotFoundError):
            return errors.get("FileNotFound")
        elif isinstance(exception_error, PermissionError):
            return errors.get("PermissionDenied")
        elif isinstance(exception_error, IsADirectoryError):
            return errors.get("IsADirectory")
        elif isinstance(exception_error, IOError):
            return errors.get("IOError")
        elif isinstance(exception_error, ValueError):
            return errors.get("ValueError")
        elif isinstance(exception_error, TypeError):
            return errors.get("TypeError")
        elif isinstance(exception_error, MemoryError):
            return errors.get("MemoryError")
        elif isinstance(exception_error, TimeoutError):
            return errors.get("TimeoutError")
        else:
            return errors.get("UnexpectedError")