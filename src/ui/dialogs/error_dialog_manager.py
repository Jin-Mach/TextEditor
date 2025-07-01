import json
import pathlib
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QFormLayout, QHBoxLayout, QPushButton, QMessageBox

from src.utilities.logging_manager import setup_logger


# noinspection PyUnresolvedReferences
class ErrorDialogManager:
    def __init__(self, parent=None) -> None:
        self.parent = parent

    def show_language_error_dialog(self, supported_languages: list) -> str | None:
        if not supported_languages:
            ErrorDialogManager.show_empty_languages_warning()
            return None
        else:
            dialog = QDialog()
            ErrorDialogManager.set_existing_icon(dialog)
            dialog.setWindowTitle("Language error")
            dialog.setFixedSize(400, 150)
            main_layout = QVBoxLayout()
            text_label = QLabel("Application doesn't support OS language.\n"
                                "Select supported language or exit application")
            text_label.setFont(QFont("Arial", 15))
            text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            select_layout = QFormLayout()
            form_text = QLabel("Selected language:")
            self.language_combobox = QComboBox()
            self.language_combobox.setFixedSize(200, 30)
            self.language_items = self.set_language_name(supported_languages)
            self.language_combobox.addItems(self.language_items.keys())
            select_layout.addRow(form_text, self.language_combobox)
            buttons_layout = QHBoxLayout()
            continue_button = QPushButton("Continue")
            continue_button.setToolTip("Open application with selected language")
            continue_button.setToolTipDuration(5000)
            continue_button.clicked.connect(dialog.accept)
            exit_button = QPushButton("Exit")
            exit_button.setToolTip("Exit application")
            exit_button.setToolTipDuration(5000)
            exit_button.clicked.connect(dialog.reject)
            buttons_layout.addStretch()
            buttons_layout.addWidget(continue_button)
            buttons_layout.addWidget(exit_button)
            main_layout.addWidget(text_label)
            main_layout.addLayout(select_layout)
            main_layout.addLayout(buttons_layout)
            dialog.setLayout(main_layout)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                return self.language_items.get(self.language_combobox.currentText())
            else:
                sys.exit(0)

    @staticmethod
    def show_empty_languages_warning() -> None:
        message_box = QMessageBox()
        ErrorDialogManager.set_existing_icon(message_box)
        message_box.setWindowTitle("Supported languages not found")
        message_box.setText("Could not find a supported language. "
                        "Please check the <a href='https://github.com/Jin-Mach/TextEditor'>please visit our GitHub repository</a> for more information.")
        message_box.exec()

    @staticmethod
    def show_simple_error_messagebox(exception: Exception) -> None:
        message_box = QMessageBox()
        ErrorDialogManager.set_existing_icon(message_box)
        message_box.setWindowTitle("Unexpected error")
        message_box.setText(f"Error: {str(exception)}")
        if message_box.exec():
            sys.exit(1)

    @staticmethod
    def set_existing_icon(dialog: QDialog | QMessageBox) -> None:
        window_icon = pathlib.Path(__file__).parent.parent.parent.joinpath("icons", "dialog_icons", "loading.png")
        if window_icon.exists():
            dialog.setWindowIcon(QIcon(window_icon))

    @staticmethod
    def set_language_name(languages: list) -> dict | None:
        try:
            language_dict = {}
            for language in languages:
                with open(str(pathlib.Path(__file__).parent.parent.parent.joinpath("config", str(language), "language_info.json")), "r", encoding="utf-8") as file:
                    language_info = json.load(file)
                    language_name = list(language_info.values())[0]
                    language_dict[language_name] = language
            return language_dict
        except Exception as e:
            logger = setup_logger()
            logger.error("An error occurred: %s", e, exc_info=True)
            ErrorDialogManager.show_empty_languages_warning(e)
            return None