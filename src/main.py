import pathlib
import sys

from PyQt6.QtWidgets import QApplication, QMessageBox

from src.ui.main_window import MainWindow
from src.utilities.logging_manager import setup_logger

def create_app():
    application = QApplication(sys.argv)

    style_file_path = pathlib.Path(__file__).parent.joinpath("style", "styles.qss")
    try:
        with open(style_file_path, "r") as file:
            application.setStyleSheet(file.read())
    except Exception as e:
        setup_logger().error(str(e))

        message_box = QMessageBox()
        message_box.setWindowTitle("Error Loading Styles")
        message_box.setIcon(QMessageBox.Icon.Critical)
        message_box.setText(
            f"Unable to load 'styles.qss'.\n"
            f"Some features (like print preview, printing) may not work correctly.\n"
            f"Please check the file location: {style_file_path}")

        continue_button = message_box.addButton("Continue", QMessageBox.ButtonRole.AcceptRole)
        continue_button.setToolTip("Opens the editor without styles.")
        continue_button.setToolTipDuration(5000)
        cancel_button = message_box.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
        cancel_button.setToolTip("Closes the dialog and exits the application.")
        cancel_button.setToolTipDuration(5000)

        message_box.exec()

        if message_box.clickedButton() == cancel_button:
            sys.exit(1)

    window = MainWindow()
    window.show()
    sys.exit(application.exec())