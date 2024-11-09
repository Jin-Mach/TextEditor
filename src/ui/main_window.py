import pathlib

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow

from src.ui.widgets.file_toolbar import FileToolbar
from src.ui.widgets.text_toolbar import TextToolbar
from src.ui.widgets.text_edit import TextEdit
from src.ui.widgets.status_bar import StatusBar
from src.utilities.data_provider import DataProvider
from src.utilities.dialog_manager import DialogManager
from src.utilities.exception_manager import ExceptionManager
from src.utilities.file_manager import FileManager
from src.utilities.messagebox_manager import MessageboxManager


class MainWindow(QMainWindow):
    application_icon = pathlib.Path(__file__).parent.parent.joinpath("icons", "application_icon.png")

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowIcon(QIcon(str(self.application_icon)))
        self.setWindowTitle("Text Editor")
        self.setMinimumSize(1400, 800)
        self.ui_text = DataProvider.get_ui_text("dialog")
        self.status_bar = StatusBar(self)
        self.text_edit = TextEdit(self.status_bar, self)
        self.file_toolbar = FileToolbar(self.text_edit, self)
        self.text_toolbar = TextToolbar(self.text_edit, self)
        self.addToolBar(self.file_toolbar)
        self.addToolBarBreak()
        self.addToolBar(self.text_toolbar)
        self.create_gui()
        self.setStatusBar(self.status_bar)

    def create_gui(self) -> None:
        central_widget = self.text_edit
        self.setCentralWidget(central_widget)

    def closeEvent(self, event) -> None:
        try:
            if self.text_edit.toPlainText():
                messagebox_manager = MessageboxManager(self)
                result = messagebox_manager.show_save_question_message()
                if result == "dontSave":
                    event.accept()
                elif result == "saveAs":
                    dialog = DialogManager(self)
                    file_path = dialog.save_document_dialog(f"{self.ui_text.get("fileFilter")}")
                    if file_path:
                        file_manager = FileManager(self.text_edit, self)
                        file_manager.save_document(file_path, "txt")
                        event.accept()
                    else:
                        event.ignore()
                elif result == "cancel":
                    event.ignore()
            else:
                event.accept()
        except Exception as e:
            ExceptionManager.exception_handler(e)