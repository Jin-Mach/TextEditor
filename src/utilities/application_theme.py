import pathlib

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication

from src.utilities.logging_manager import setup_logger
from src.ui.dialogs.messagebox_manager import MessageboxManager


class ApplicationTheme:

    @staticmethod
    def set_light_theme(application: QApplication, parent=None):
        style_file_path = pathlib.Path(__file__).parent.parent.joinpath("style", "styles.qss")
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#F0F0F0"))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)
        palette.setColor(QPalette.ColorRole.Base, QColor("#FFFFFF"))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#E0E0E0"))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#FFFFFF"))
        palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.black)
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.black)
        palette.setColor(QPalette.ColorRole.Button, QColor("#E0E0E0"))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.black)
        palette.setColor(QPalette.ColorRole.Highlight, QColor("#87CEFA"))
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
        application.setPalette(palette)
        if style_file_path.exists():
            try:
                with open(style_file_path, "r", encoding="utf-8") as file:
                    application.setStyleSheet(file.read())
            except Exception as e:
                setup_logger().error(str(e))
                messagebox_manager = MessageboxManager(parent)
                messagebox_manager.show_load_error_message(e, str(style_file_path))