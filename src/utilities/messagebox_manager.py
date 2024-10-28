import pathlib
import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMessageBox, QApplication, QPushButton

from src.utilities.decoration_manager import DecorationManager


class MessageboxManager:
    def __init__(self) -> None:
        self.icons_path = pathlib.Path(__file__).parent.parent.joinpath("icons", "dialog_icons")

    def show_load_error_message(self, style_file_path: str) -> None:
        message_box = QMessageBox()
        message_box.setWindowIcon(QIcon(str(self.icons_path.joinpath("loading.png"))))
        message_box.setWindowTitle("Error Loading Styles")
        message_box.setIcon(QMessageBox.Icon.Critical)
        message_box.setText(
            f"Unable to load 'styles.qss'.\n"
            f"Some features (like print preview, printing, etc.) may not work correctly.\n"
            f"Please check the file location: {style_file_path}")
        self.continue_button = message_box.addButton("Continue", QMessageBox.ButtonRole.AcceptRole)
        self.continue_button.setObjectName("applicationContinue")
        self.cancel_button = message_box.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
        self.cancel_button.setObjectName("applicationCancel")
        self.set_tooltips(message_box)
        message_box.exec()
        if message_box.clickedButton() == self.cancel_button:
            sys.exit(1)

    def show_error_message(self, error_message: str, parent=None) -> None:
        message_box = QMessageBox(parent)
        message_box.setWindowTitle("Error")
        message_box.setWindowIcon(QIcon(str(self.icons_path.joinpath("error.png"))))
        message_box.setText(error_message)
        self.copy_button = message_box.addButton("Copy", QMessageBox.ButtonRole.AcceptRole)
        self.copy_button.setObjectName("errorCopy")
        self.cancel_button = message_box.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
        self.cancel_button.setObjectName("errorCancel")
        self.set_tooltips(message_box)
        message_box.exec()
        if message_box.clickedButton() == self.copy_button:
            QApplication.clipboard().setText(error_message)
            message_box.close()

    def set_tooltips(self, parent):
        tooltips = DecorationManager.get_tooltips("messagebox_tooltips")
        for button in parent.findChildren(QPushButton):
            if button.objectName() in tooltips:
                tooltips_text = tooltips.get(button.objectName())
                button.setToolTip(tooltips_text)
                button.setToolTipDuration(5000)