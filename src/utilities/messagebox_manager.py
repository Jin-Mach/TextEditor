import pathlib
import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMessageBox, QApplication, QPushButton

from src.utilities.data_provider import DataProvider


class MessageboxManager:
    def __init__(self) -> None:
        self.icons_path = pathlib.Path(__file__).parent.parent.joinpath("icons", "dialog_icons")

    def show_load_error_message(self, exception_error: Exception, style_file_path: str) -> None:
        ui_text = DataProvider.get_ui_text("messagebox")
        message_box = QMessageBox()
        message_box.setWindowIcon(QIcon(str(self.icons_path.joinpath("loading.png"))))
        message_box.setWindowTitle(ui_text.get("loadingError"))
        message_box.setIcon(QMessageBox.Icon.Critical)
        message_box.setText(self.set_error_text(exception_error) + "\n" + style_file_path)
        self.continue_button = message_box.addButton(ui_text.get("applicationContinue"), QMessageBox.ButtonRole.AcceptRole)
        self.continue_button.setObjectName("applicationContinue")
        self.cancel_button = message_box.addButton(ui_text.get("applicationCancel"), QMessageBox.ButtonRole.RejectRole)
        self.cancel_button.setObjectName("applicationCancel")
        self.set_tooltips(message_box)
        message_box.exec()
        if message_box.clickedButton() == self.cancel_button:
            sys.exit(1)

    def show_error_message(self, exception_error: Exception, parent=None) -> None:
        ui_text = DataProvider.get_ui_text("messagebox")
        message_box = QMessageBox(parent)
        message_box.setWindowTitle(ui_text.get("errorMessage"))
        message_box.setWindowIcon(QIcon(str(self.icons_path.joinpath("error.png"))))
        message_box.setText(self.set_error_text(exception_error))
        self.copy_button = message_box.addButton(ui_text.get("errorCopy"), QMessageBox.ButtonRole.AcceptRole)
        self.copy_button.setObjectName("errorCopy")
        self.cancel_button = message_box.addButton(ui_text.get("errorCancel"), QMessageBox.ButtonRole.RejectRole)
        self.cancel_button.setObjectName("errorCancel")
        self.set_tooltips(message_box)
        message_box.exec()
        if message_box.clickedButton() == self.copy_button:
            QApplication.clipboard().setText(self.set_error_text(exception_error))
            message_box.close()

    def set_tooltips(self, parent) -> None:
        tooltips = DataProvider.get_tooltips("messagebox_tooltips")
        for button in parent.findChildren(QPushButton):
            if button.objectName() in tooltips:
                tooltips_text = tooltips.get(button.objectName())
                button.setToolTip(tooltips_text)
                button.setToolTipDuration(5000)

    def set_error_text(self, exception_error: Exception) -> str:
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