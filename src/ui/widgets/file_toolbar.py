import pathlib

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QToolBar, QWidget, QPushButton, QHBoxLayout, QLabel, QLineEdit, QTextEdit
from src.utilities.data_provider import DataProvider
from src.utilities.file_manager import Filemanager


# noinspection PyUnresolvedReferences
class FileToolbar(QToolBar):
    ui_text = DataProvider.get_ui_text("fileToolbar")

    def __init__(self, text_edit: QTextEdit, parent=None) -> None:
        super().__init__(parent)
        self.text_edit = text_edit
        self.file_manager = Filemanager(self.text_edit, self)
        self.setObjectName("fileToolbar")
        self.setAllowedAreas(Qt.ToolBarArea.TopToolBarArea)
        self.setOrientation(Qt.Orientation.Horizontal)
        self.setFloatable(False)
        self.setMovable(False)
        self.create_main_gui()
        self.set_icons()
        self.set_ui_text()
        self.set_tooltips()

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
        self.new_file_button.clicked.connect(self.file_manager.new_file)
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
                button.setIconSize(QSize(20, 20))

    def set_tooltips(self) -> None:
        tooltips = DataProvider.get_tooltips("fileTooltips")
        for button in self.findChildren(QPushButton):
            if button.objectName() in tooltips:
                tooltips_text = tooltips.get(button.objectName())
                button.setToolTip(tooltips_text)
                button.setToolTipDuration(5000)

    def set_ui_text(self) -> None:
        self.search_label.setText(self.ui_text.get("searchLabel"))
        self.search_input.setPlaceholderText(self.ui_text.get("searchLineedit")["placeholderText"])