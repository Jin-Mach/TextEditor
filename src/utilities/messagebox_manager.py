import json
import pathlib
import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMessageBox, QApplication, QWidget


class MessageboxManager:
    icons_path = pathlib.Path(__file__).parent.parent.joinpath("icons")
    tooltips_path = pathlib.Path(__file__).parent.parent.joinpath("config", "tooltips", "tooltips_en.json")

    @staticmethod
    def load_tooltips() -> dict:
        with open(str(MessageboxManager.tooltips_path), "r", encoding="utf-8") as file:
            tooltips = json.load(file)
            return tooltips["messagebox_tooltips"]

    @staticmethod
    def set_tooltips(widget: QWidget, tooltip_key: str) -> None:
        tooltips_text = MessageboxManager.load_tooltips().get(tooltip_key)
        widget.setToolTip(tooltips_text)
        widget.setToolTipDuration(5000)

    @staticmethod
    def show_load_error_message(style_file_path: str) -> None:
        message_box = QMessageBox()
        message_box.setWindowIcon(QIcon(str(MessageboxManager.icons_path.joinpath("loading_error_icon.png"))))
        message_box.setWindowTitle("Error Loading Styles")
        message_box.setIcon(QMessageBox.Icon.Critical)
        message_box.setText(
            f"Unable to load 'styles.qss'.\n"
            f"Some features (like print preview, printing, etc.) may not work correctly.\n"
            f"Please check the file location: {style_file_path}")

        continue_button = message_box.addButton("Continue", QMessageBox.ButtonRole.AcceptRole)
        MessageboxManager.set_tooltips(continue_button, "application_continue_button")
        cancel_button = message_box.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
        MessageboxManager.set_tooltips(cancel_button, "application_cancel_button")

        message_box.exec()

        if message_box.clickedButton() == cancel_button:
            sys.exit(1)

    @staticmethod
    def show_error_message(error_message: str, parent=None) -> None:
        message_box = QMessageBox(parent)
        message_box.setWindowTitle("Error")
        message_box.setWindowIcon(QIcon(str(MessageboxManager.icons_path.joinpath("error_icon.png"))))
        message_box.setText(error_message)
        copy_button = message_box.addButton("Copy", QMessageBox.ButtonRole.AcceptRole)
        MessageboxManager.set_tooltips(copy_button, "error_copy_button")
        cancel_button = message_box.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
        MessageboxManager.set_tooltips(cancel_button, "error_cancel_button")

        message_box.exec()

        if message_box.clickedButton() == copy_button:
            QApplication.clipboard().setText(error_message)
            message_box.close()