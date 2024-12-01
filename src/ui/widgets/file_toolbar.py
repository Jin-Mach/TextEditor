import pathlib
from typing import Optional

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QToolBar, QWidget, QPushButton, QHBoxLayout, QLabel, QLineEdit, QSystemTrayIcon, QMenuBar

from src.ui.widgets.text_edit import TextEdit
from src.utilities.data_provider import DataProvider
from src.utilities.file_manager import FileManager
from src.utilities.find_manager import FindManager
from src.utilities.print_manager import Printmanager


# noinspection PyUnresolvedReferences
class FileToolbar(QToolBar):
    def __init__(self, text_edit: TextEdit, tray_icon: QSystemTrayIcon, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("fileToolbar")
        self.tray_icon_ui_text = DataProvider.get_ui_text("trayicon")
        self.parent = parent
        self.text_edit = text_edit
        self.tray_icon = tray_icon
        self.file_manager = FileManager(self.text_edit, tray_icon, self)
        self.print_manager = Printmanager(self.text_edit, self.parent)
        self.setAllowedAreas(Qt.ToolBarArea.TopToolBarArea)
        self.setOrientation(Qt.Orientation.Horizontal)
        self.setFloatable(False)
        self.setMovable(False)
        self.create_main_gui()
        self.set_icons()
        self.set_ui_text()
        self.set_tooltips()
        self.find_manager = FindManager(self.search_input, self.text_edit)
        self.create_connection()

    def create_main_gui(self) -> None:
        self.addWidget(self.create_file_widget())
        self.addSeparator()
        self.addWidget(self.create_export_widget())
        self.addSeparator()
        self.addWidget(self.create_print_widget())
        self.addSeparator()
        self.addWidget(self.create_search_widget())

    def create_file_widget(self) -> QWidget:
        file_widget = QWidget()
        file_layout = QHBoxLayout()
        self.new_file_button = QPushButton()
        self.new_file_button.setObjectName("newFile")
        self.open_file_button = QPushButton()
        self.open_file_button.setObjectName("openFile")
        self.save_as_button = QPushButton()
        self.save_as_button.setObjectName("saveAs")
        self.save_button = QPushButton()
        self.save_button.setObjectName("save")
        self.save_button.setDisabled(True)
        file_layout.addWidget(self.new_file_button)
        file_layout.addWidget(self.open_file_button)
        file_layout.addWidget(self.save_as_button)
        file_layout.addWidget(self.save_button)
        file_widget.setLayout(file_layout)
        return file_widget

    def create_export_widget(self) -> QWidget:
        export_widget = QWidget()
        export_layout = QHBoxLayout()
        self.save_as_html_button = QPushButton()
        self.save_as_html_button.setObjectName("saveHtml")
        self.export_pdf_button = QPushButton()
        self.export_pdf_button.setObjectName("exportPdf")
        export_layout.addWidget(self.save_as_html_button)
        export_layout.addWidget(self.export_pdf_button)
        export_widget.setLayout(export_layout)
        return export_widget

    def create_print_widget(self) -> QWidget:
        print_widget = QWidget()
        print_layout = QHBoxLayout()
        self.print_preview_button = QPushButton()
        self.print_preview_button.setObjectName("printPreview")
        self.print_button = QPushButton()
        self.print_button.setObjectName("print")
        print_layout.addWidget(self.print_preview_button)
        print_layout.addWidget(self.print_button)
        print_widget.setLayout(print_layout)
        return print_widget

    def create_search_widget(self) -> QWidget:
        search_widget = QWidget()
        search_layout = QHBoxLayout()
        self.search_label = QLabel()
        self.search_label.setObjectName("searchLabel")
        self.search_input = QLineEdit()
        self.search_input.setObjectName("searchLineedit")
        self.search_button = QPushButton()
        self.search_button.setObjectName("search")
        search_layout.addWidget(self.search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        search_layout.addStretch()
        search_widget.setLayout(search_layout)
        return search_widget

    def set_icons(self) -> None:
        icons_dict = DataProvider.get_icons(pathlib.Path(__file__).parent.parent.parent.joinpath("icons", "file_icons"))
        buttons = self.findChildren(QPushButton)
        for button in buttons:
            name = button.objectName()
            if name in icons_dict.keys():
                button.setIcon(QIcon(str(icons_dict[name])))
                button.setIconSize(QSize(25, 25))

    def set_tooltips(self) -> None:
        tooltips = DataProvider.get_tooltips("fileTooltips")
        for button in self.findChildren(QPushButton):
            if button.objectName() in tooltips:
                tooltips_text = tooltips.get(button.objectName())
                button.setToolTip(tooltips_text)
                button.setToolTipDuration(5000)

    def set_ui_text(self) -> None:
        ui_text = DataProvider.get_ui_text("fileToolbar")
        self.search_label.setText(ui_text.get("searchLabel"))
        self.search_input.setPlaceholderText(ui_text.get("searchLineedit")["placeholderText"])

    def create_connection(self) -> None:
        self.new_file_button.clicked.connect(self.new_file)
        self.open_file_button.clicked.connect(self.open_file)
        self.save_as_button.clicked.connect(lambda: self.save_file(".txt"))
        self.save_button.clicked.connect(lambda: self.save_file(None))
        self.save_as_html_button.clicked.connect(lambda: self.save_file(".html"))
        self.export_pdf_button.clicked.connect(lambda: self.save_file(".pdf"))
        self.print_preview_button.clicked.connect(self.print_manager.show_print_preview)
        self.print_button.clicked.connect(self.print_manager.print_document)
        self.search_button.clicked.connect(self.find_manager.find_text)

    def reset_file_toolbar(self) -> None:
        self.save_button.setDisabled(True)

    def new_file(self) -> None:
        self.file_manager.new_file(self.parent.findChild(QMenuBar, "menuBar"), self)
        self.parent.findChild(QMenuBar, "menuBar").reset_menu_bar()
        self.reset_file_toolbar()
        self.parent.findChild(QToolBar, "textToolbar").reset_text_toolbar()

    def open_file(self) -> None:
        self.file_manager.open_file(self.parent.findChild(QMenuBar, "menuBar"), self)
        self.save_button.setDisabled(False)
        self.parent.findChild(QMenuBar, "menuBar").save_action.setDisabled(False)
        self.parent.findChild(QToolBar, "textToolbar").reset_text_toolbar()

    def save_file(self, file_type: Optional[str]) -> None:
        if file_type is None:
            self.file_manager.save_file()
        else:
            self.file_manager.save_file_as(self.parent.findChild(QMenuBar, "menuBar"), self, file_type)