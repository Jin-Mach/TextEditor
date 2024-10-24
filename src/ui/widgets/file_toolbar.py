from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QToolBar, QWidget, QPushButton, QHBoxLayout, QLabel, QLineEdit


class FileToolbar(QToolBar):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("fileToolbar")
        self.setAllowedAreas(Qt.ToolBarArea.TopToolBarArea)
        self.setOrientation(Qt.Orientation.Horizontal)
        self.setFloatable(False)
        self.setMovable(False)
        self.addWidget(self.create_file_widget())
        self.addSeparator()
        self.addWidget(self.create_export_widget())
        self.addSeparator()
        self.addWidget(self.create_print_widget())
        self.addSeparator()
        self.addWidget(self.create_find_widget())

    def create_file_widget(self) -> QWidget:
        file_widget = QWidget()
        file_layout = QHBoxLayout()
        new_file_button = QPushButton()
        open_file_button = QPushButton()
        save_as_button = QPushButton()
        self.save_button = QPushButton()
        self.save_button.setDisabled(True)
        close_button = QPushButton()
        file_layout.addWidget(new_file_button)
        file_layout.addWidget(open_file_button)
        file_layout.addWidget(save_as_button)
        file_layout.addWidget(self.save_button)
        file_layout.addWidget(close_button)
        file_widget.setLayout(file_layout)
        return file_widget

    def create_export_widget(self) -> QWidget:
        export_widget = QWidget()
        export_layout = QHBoxLayout()
        save_as_html_button = QPushButton()
        export_pdf_button = QPushButton()
        export_layout.addWidget(save_as_html_button)
        export_layout.addWidget(export_pdf_button)
        export_widget.setLayout(export_layout)
        return export_widget

    def create_print_widget(self) -> QWidget:
        print_widget = QWidget()
        print_layout = QHBoxLayout()
        print_preview_button = QPushButton()
        print_button = QPushButton()
        print_layout.addWidget(print_preview_button)
        print_layout.addWidget(print_button)
        print_widget.setLayout(print_layout)
        return print_widget

    def create_find_widget(self) -> QWidget:
        find_widget = QWidget()
        find_layout = QHBoxLayout()
        find_label = QLabel("Find:")
        self.find_input = QLineEdit()
        find_button = QPushButton()
        find_layout.addWidget(find_label)
        find_layout.addWidget(self.find_input)
        find_layout.addWidget(find_button)
        find_layout.addStretch()
        find_widget.setLayout(find_layout)
        return find_widget