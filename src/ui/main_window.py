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
        self.file_toolbar = FileToolbar(self)
        self.text_toolbar = TextToolbar(self)
        self.status_bar = StatusBar(self)
        self.addToolBar(self.file_toolbar)
        self.addToolBarBreak()
        self.addToolBar(self.text_toolbar)
        self.setStatusBar(self.status_bar)
        self.create_gui()
        self.text_edit.setFocus()

    def create_gui(self) -> None:
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        self.text_edit = TextEdit(self)
        main_layout.addWidget(self.text_edit)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)