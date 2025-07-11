from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow

from src.ui.widgets.file_toolbar import FileToolbar
from src.ui.widgets.menu_bar import MenuBar
from src.ui.widgets.text_toolbar import TextToolbar
from src.ui.widgets.text_edit import TextEdit
from src.ui.widgets.status_bar import StatusBar
from src.utilities.data_provider import DataProvider
from src.ui.dialogs.file_dialog_manager import FileDialogManager
from src.utilities.exception_manager import ExceptionManager
from src.utilities.file_manager import FileManager
from src.ui.dialogs.messagebox_manager import MessageboxManager
from src.utilities.print_manager import PrintManager
from src.utilities.settings_manager import SettingsManager
from src.utilities.text_manager import TextManager
from src.utilities.tray_icon import TrayIcon


class MainWindow(QMainWindow):
    default_window_size = QSize(1400, 800)

    def __init__(self, language_code: str, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Text Editor")
        self.setMinimumSize(self.default_window_size)
        self.language_code = language_code
        self.ui_text = DataProvider.get_ui_text("dialog", self.language_code)
        self.status_bar = StatusBar(self.language_code, self)
        self.text_edit = TextEdit(self.language_code, self.status_bar, self)
        self.tray_icon = TrayIcon(self.language_code, self)
        self.print_manager = PrintManager(self.language_code, self.text_edit, self)
        self.file_manager = FileManager(self.language_code, self.text_edit, self.tray_icon, self)
        self.text_manager = TextManager(self.text_edit, self)
        self.menu_bar = MenuBar(self.language_code, self.text_edit, self.file_manager, self.print_manager, self.text_manager, self)
        self.file_toolbar = FileToolbar(self.language_code, self.text_edit, self.file_manager, self.print_manager, self.tray_icon, self)
        self.text_toolbar = TextToolbar(self.language_code, self.text_edit, self)
        self.addToolBar(self.file_toolbar)
        self.addToolBarBreak()
        self.addToolBar(self.text_toolbar)
        self.create_gui()
        self.setMenuBar(self.menu_bar)
        self.setStatusBar(self.status_bar)
        self.tray_icon.create_connection()
        SettingsManager.load_settings(self, self.default_window_size)

    def create_gui(self) -> None:
        central_widget = self.text_edit
        self.setCentralWidget(central_widget)

    def closeEvent(self, event) -> None:
        try:
            if not self.text_edit.document().isModified() or not self.text_edit.toPlainText().strip():
                event.accept()
                SettingsManager.save_settings(self)
            else:
                messagebox_manager = MessageboxManager(self)
                result = messagebox_manager.show_save_question_message()
                if result == "dontSave":
                    event.accept()
                    SettingsManager.save_settings(self)
                elif result == "saveAs":
                    dialog = FileDialogManager(self)
                    file_path = dialog.save_document_dialog(f"{self.ui_text.get("fileFilter")}")
                    if file_path:
                        self.file_manager.save_document(file_path, ".txt")
                        event.accept()
                        SettingsManager.save_settings(self)
                    else:
                        event.ignore()
                elif result == "cancel":
                    event.ignore()
        except Exception as e:
            ExceptionManager.exception_handler(e)