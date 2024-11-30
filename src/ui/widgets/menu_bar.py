from typing import Optional

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenuBar, QMenu, QTextEdit, QToolBar, QSystemTrayIcon

from src.utilities.data_provider import DataProvider
from src.utilities.file_manager import FileManager
from src.utilities.print_manager import Printmanager


# noinspection PyUnresolvedReferences
class MenuBar(QMenuBar):
    def __init__(self, text_edit: QTextEdit, file_manager: FileManager, tray_icon: QSystemTrayIcon, parent=None):
        super().__init__(parent)
        self.setObjectName("menuBar")
        self.tray_icon_ui_text = DataProvider.get_ui_text("trayicon")
        self.parent = parent
        self.text_edit = text_edit
        self.file_manager = file_manager
        self.tray_icon = tray_icon
        self.toolbar = self.parent.findChild(QToolBar, "fileToolbar")
        self.create_gui()
        self.set_ui_text()
        self.create_connection()
        self.show()

    def create_gui(self) -> None:
        file_menu = QMenu("Soubor", self)
        self.new_file_action = QAction(self)
        self.new_file_action.setObjectName("newFile")
        self.open_file_action = QAction(self)
        self.open_file_action.setObjectName("openFile")
        self.save_as_action = QAction(self)
        self.save_as_action.setObjectName("saveAs")
        self.save_action = QAction(self)
        self.save_action.setObjectName("save")
        self.save_action.setDisabled(True)
        self.save_as_html_action = QAction(self)
        self.save_as_html_action.setObjectName("saveasHtml")
        self.save_as_pdf_action = QAction(self)
        self.save_as_pdf_action.setObjectName("saveasPdf")
        self.print_preview_action = QAction(self)
        self.print_preview_action.setObjectName("printPreview")
        self.print_document_action = QAction(self)
        self.print_document_action.setObjectName("printDocument")
        self.close_application_action = QAction(self)
        self.close_application_action.setObjectName("closeApplication")
        file_menu.addAction(self.new_file_action)
        file_menu.addAction(self.open_file_action)
        file_menu.addAction(self.save_as_action)
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.save_as_html_action)
        file_menu.addAction(self.save_as_pdf_action)
        file_menu.addSeparator()
        file_menu.addAction(self.close_application_action)
        self.addMenu(file_menu)

    def set_ui_text(self) -> None:
        actions = [self.new_file_action, self.open_file_action, self.save_as_action, self.save_action, self.save_as_html_action, self.save_as_pdf_action, self.print_preview_action,
                   self.print_document_action, self.close_application_action]
        ui_text = DataProvider.get_ui_text("menubar")
        for action in actions:
            action.setText(ui_text.get(action.objectName()))

    def create_connection(self) -> None:
        print_manager = Printmanager(self.parent.findChild(QTextEdit, "textEdit"), self.parent)
        self.new_file_action.triggered.connect(self.new_file)
        self.open_file_action.triggered.connect(self.open_file)
        self.save_as_action.triggered.connect(lambda: self.save_file(".txt"))
        self.save_action.triggered.connect(lambda: self.save_file(None))
        self.save_as_html_action.triggered.connect(lambda: self.save_file(".html"))
        self.save_as_pdf_action.triggered.connect(lambda: self.save_file(".pdf"))
        self.print_preview_action.triggered.connect(print_manager.show_print_preview)
        self.print_document_action.triggered.connect(print_manager.print_document)
        self.close_application_action.triggered.connect(self.close_application)

    def new_file(self) -> None:
        file_toolbar = self.parent.findChild(QToolBar, "fileToolbar")
        text_toolbar = self.parent.findChild(QToolBar, "textToolbar")
        self.file_manager.new_file()
        self.reset_menu_bar()
        file_toolbar.reset_file_toolbar()
        text_toolbar.reset_text_toolbar()
        self.text_edit.reset_text_edit()

    def open_file(self) -> None:
        self.file_toolbar = self.parent.findChild(QToolBar, "fileToolbar")
        self.text_toolbar = self.parent.findChild(QToolBar, "textToolbar")
        result = self.file_manager.open_file()
        if result:
            self.save_action.setDisabled(False)
            self.file_toolbar.save_button.setDisabled(False)
            self.text_toolbar.reset_text_toolbar()

    def save_file(self, file_type: Optional[str]) -> None:
        if file_type is None:
            self.file_manager.save_file()
            self.tray_icon.showMessage(self.tray_icon_ui_text.get("saveTitle"), self.tray_icon_ui_text.get("saveText"))
        else:
            if self.file_manager.save_file_as(file_type):
                self.tray_icon.showMessage(self.tray_icon_ui_text.get("saveTitle"), self.tray_icon_ui_text.get("saveText"))

    def close_application(self) -> None:
        main_window = self.parent
        main_window.close()

    def reset_menu_bar(self) -> None:
        self.save_action.setDisabled(True)