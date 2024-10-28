import pathlib

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout

from src.ui.widgets.file_toolbar import FileToolbar
from src.ui.widgets.text_toolbar import TextToolbar
from src.ui.widgets.text_edit import TextEdit
from src.ui.widgets.status_bar import StatusBar


class MainWindow(QMainWindow):
    application_icon = pathlib.Path(__file__).parent.parent.joinpath("icons", "application_icon.png")

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowIcon(QIcon(str(self.application_icon)))
        self.setWindowTitle("Text Editor")
        self.setMinimumSize(1400, 800)
        self.status_bar = StatusBar(self)
        self.text_edit = TextEdit(self.status_bar, self)
        self.file_toolbar = FileToolbar(self)
        self.text_toolbar = TextToolbar(self)
        self.addToolBar(self.file_toolbar)
        self.addToolBarBreak()
        self.addToolBar(self.text_toolbar)
        self.create_gui()
        self.setStatusBar(self.status_bar)
        self.text_edit.setFocus()

    def create_gui(self) -> None:
        central_widget = self.text_edit
        self.setCentralWidget(central_widget)