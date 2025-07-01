import pathlib

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QGuiApplication, QIcon, QKeySequence
from PyQt6.QtWidgets import QMenuBar, QMenu, QToolBar

from src.ui.widgets.text_edit import TextEdit
from src.utilities.data_provider import DataProvider
from src.utilities.file_manager import FileManager
from src.utilities.print_manager import PrintManager
from src.utilities.text_manager import TextManager


# noinspection PyUnresolvedReferences
class MenuBar(QMenuBar):
    def __init__(self, language_code: str, text_edit: TextEdit, file_manager: FileManager, print_manager: PrintManager, text_manager: TextManager, parent=None):
        super().__init__(parent)
        self.setObjectName("menuBar")
        self.language_code = language_code
        self.parent = parent
        self.text_edit = text_edit
        self.file_manager = file_manager
        self.print_manager = print_manager
        self.text_manager = text_manager
        self.create_file_menu()
        self.create_edit_menu()
        self.create_format_menu()
        self.set_menus_ui_text()
        self.set_actions_ui_text()
        self.set_icons()
        self.create_connection()
        self.set_shortcuts()
        self.update_edit_menu()
        self.show()
        self.text_edit.cursorPositionChanged.connect(self.update_edit_menu)

    def create_file_menu(self) -> None:
        self.file_menu = QMenu(self)
        self.file_menu.setObjectName("fileMenu")
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
        self.save_as_html_action.setObjectName("saveHtml")
        self.save_as_pdf_action = QAction(self)
        self.save_as_pdf_action.setObjectName("exportPdf")
        self.print_preview_action = QAction(self)
        self.print_preview_action.setObjectName("printPreview")
        self.print_document_action = QAction(self)
        self.print_document_action.setObjectName("print")
        self.close_application_action = QAction(self)
        self.close_application_action.setObjectName("closeApplication")
        actions = [self.new_file_action, self.open_file_action, self.save_as_action, self.save_action, self.save_as_html_action,
                   self.save_as_pdf_action, self.print_preview_action, self.print_document_action, self.close_application_action]
        for action in actions:
            if action == self.print_preview_action or action == self.close_application_action:
                self.file_menu.addSeparator()
                self.file_menu.addAction(action)
            self.file_menu.addAction(action)
        self.addMenu(self.file_menu)

    def create_edit_menu(self) -> None:
        self.edit_menu = QMenu()
        self.edit_menu.setObjectName("editMenu")
        self.undo_action = QAction(self)
        self.undo_action.setObjectName("undo")
        self.redo_action = QAction(self)
        self.redo_action.setObjectName("redo")
        self.cut_action = QAction(self)
        self.cut_action.setObjectName("cut")
        self.copy_action = QAction(self)
        self.copy_action.setObjectName("copy")
        self.paste_action = QAction(self)
        self.paste_action.setObjectName("paste")
        self.select_action = QAction(self)
        self.select_action.setObjectName("selectAll")
        self.delete_action = QAction(self)
        self.delete_action.setObjectName("deleteText")
        actions = [self.undo_action, self.redo_action, self.cut_action, self.copy_action, self.paste_action,self.select_action,
                   self.delete_action]
        for action in actions:
            self.edit_menu.addAction(action)
        self.addMenu(self.edit_menu)

    def create_format_menu(self) -> None:
        self.format_menu = QMenu()
        self.format_menu.setObjectName("formatMenu")
        self.bold_action = QAction(self)
        self.bold_action.setObjectName("bold")
        self.italic_action = QAction(self)
        self.italic_action.setObjectName("italic")
        self.underline_action = QAction(self)
        self.underline_action.setObjectName("underline")
        self.strikeout_action = QAction(self)
        self.strikeout_action.setObjectName("strikeout")
        self.align_left_action = QAction(self)
        self.align_left_action.setObjectName("alignLeft")
        self.align_center_action = QAction(self)
        self.align_center_action.setObjectName("alignCenter")
        self.align_right_action = QAction(self)
        self.align_right_action.setObjectName("alignRight")
        self.align_justify_action = QAction(self)
        self.align_justify_action.setObjectName("alignJustify")
        actions = [self.bold_action, self.italic_action, self.underline_action, self.strikeout_action, self.align_left_action,
                   self.align_center_action, self.align_right_action, self.align_justify_action]
        for action in actions:
            if action == self.align_left_action:
                self.format_menu.addSeparator()
                self.format_menu.addAction(action)
            self.format_menu.addAction(action)
        self.addMenu(self.format_menu)

    def set_menus_ui_text(self) -> None:
        menus = [self.file_menu, self.edit_menu, self.format_menu]
        ui_text = DataProvider.get_ui_text("menubar", self.language_code)
        for menu in menus:
            menu.setTitle(ui_text.get(menu.objectName()))

    def set_actions_ui_text(self) -> None:
        actions = [self.new_file_action, self.open_file_action, self.save_as_action, self.save_action, self.save_as_html_action,
                   self.save_as_pdf_action, self.print_preview_action, self.print_document_action, self.close_application_action,
                   self.undo_action, self.redo_action, self.cut_action, self.copy_action, self.paste_action, self.select_action,
                   self.delete_action, self.bold_action, self.italic_action, self.underline_action, self.strikeout_action,
                   self.align_left_action, self.align_center_action, self.align_right_action, self.align_justify_action]
        ui_text = DataProvider.get_ui_text("menubar", self.language_code)
        for action in actions:
            action.setText(ui_text.get(action.objectName()))

    def set_icons(self) -> None:
        file_icons_path = pathlib.Path(__file__).parent.parent.parent.joinpath("icons", "file_icons")
        text_icons_path = pathlib.Path(__file__).parent.parent.parent.joinpath("icons", "text_icons")
        if file_icons_path.exists() and text_icons_path.exists():
            file_icons_dict = DataProvider.get_icons(file_icons_path)
            text_icons_dict = DataProvider.get_icons(text_icons_path)
            close_app_icon = pathlib.Path(__file__).parent.parent.parent.joinpath("icons", "closeApplication")
            if close_app_icon.exists():
                self.close_application_action.setIcon(QIcon(str(close_app_icon)))
            file_actions = [self.new_file_action, self.open_file_action, self.save_as_action, self.save_action, self.save_as_html_action,
                       self.save_as_pdf_action, self.print_preview_action, self.print_document_action, self.close_application_action]
            for action in file_actions:
                if action.objectName() in file_icons_dict.keys():
                    action.setIcon(QIcon(str(file_icons_dict[action.objectName()])))
            text_actions = [self.undo_action, self.redo_action, self.cut_action, self.copy_action, self.paste_action, self.select_action,
                            self.delete_action, self.bold_action, self.italic_action, self.underline_action, self.strikeout_action,
                            self.align_left_action, self.align_center_action, self.align_right_action, self.align_justify_action]
            for action in text_actions:
                if action.objectName() in text_icons_dict.keys():
                    action.setIcon(QIcon(str(text_icons_dict[action.objectName()])))

    def create_connection(self) -> None:
        self.new_file_action.triggered.connect(self.new_file)
        self.open_file_action.triggered.connect(self.open_file)
        self.save_as_action.triggered.connect(lambda: self.save_file(".txt"))
        self.save_action.triggered.connect(lambda: self.save_file(None))
        self.save_as_html_action.triggered.connect(lambda: self.save_file(".html"))
        self.save_as_pdf_action.triggered.connect(lambda: self.save_file(".pdf"))
        self.print_preview_action.triggered.connect(self.print_manager.show_print_preview)
        self.print_document_action.triggered.connect(self.print_manager.print_document)
        self.close_application_action.triggered.connect(self.close_application)
        self.undo_action.triggered.connect(self.text_edit.undo)
        self.redo_action.triggered.connect(self.text_edit.redo)
        self.cut_action.triggered.connect(self.text_edit.cut)
        self.copy_action.triggered.connect(self.text_edit.copy)
        self.paste_action.triggered.connect(self.text_edit.custom_paste)
        self.select_action.triggered.connect(self.text_edit.selectAll)
        self.delete_action.triggered.connect(self.text_edit.clear_text_edit)
        self.bold_action.triggered.connect(lambda: self.text_manager.set_text_format("bold"))
        self.italic_action.triggered.connect(lambda: self.text_manager.set_text_format("italic"))
        self.underline_action.triggered.connect(lambda: self.text_manager.set_text_format("underline"))
        self.strikeout_action.triggered.connect(lambda: self.text_manager.set_text_format("strikeout"))
        self.align_left_action.triggered.connect(lambda: self.text_manager.set_alignment(Qt.AlignmentFlag.AlignLeft))
        self.align_center_action.triggered.connect(lambda: self.text_manager.set_alignment(Qt.AlignmentFlag.AlignCenter))
        self.align_right_action.triggered.connect(lambda: self.text_manager.set_alignment(Qt.AlignmentFlag.AlignRight))
        self.align_justify_action.triggered.connect(lambda: self.text_manager.set_alignment(Qt.AlignmentFlag.AlignJustify))

    def set_shortcuts(self) -> None:
        self.new_file_action.setShortcut(QKeySequence("Ctrl+N"))
        self.open_file_action.setShortcut(QKeySequence("Ctrl+O"))
        self.save_as_action.setShortcut(QKeySequence("Ctrl+Shift+S"))
        self.save_action.setShortcut(QKeySequence("Ctrl+S"))
        self.save_as_html_action.setShortcut(QKeySequence("Ctrl+Alt+H"))
        self.save_as_pdf_action.setShortcut(QKeySequence("Ctrl+Alt+P"))
        self.print_preview_action.setShortcut(QKeySequence("Ctrl+Shift+P"))
        self.print_document_action.setShortcut(QKeySequence("Ctrl+P"))
        self.close_application_action.setShortcut(QKeySequence("Ctrl+Q"))
        self.undo_action.setShortcut(QKeySequence("Ctrl+Z"))
        self.redo_action.setShortcut(QKeySequence("Ctrl+Y"))
        self.cut_action.setShortcut(QKeySequence("Ctrl+X"))
        self.copy_action.setShortcut(QKeySequence("Ctrl+C"))
        self.paste_action.setShortcut(QKeySequence("Ctrl+V"))
        self.select_action.setShortcut(QKeySequence("Ctrl+A"))
        self.delete_action.setShortcut(QKeySequence("Ctrl+Shift+Delete"))
        self.bold_action.setShortcut(QKeySequence("Ctrl+B"))
        self.italic_action.setShortcut(QKeySequence("Ctrl+I"))
        self.underline_action.setShortcut(QKeySequence("Ctrl+U"))
        self.strikeout_action.setShortcut(QKeySequence("Ctrl+Shift+X"))
        self.align_left_action.setShortcut(QKeySequence("Ctrl+L"))
        self.align_center_action.setShortcut(QKeySequence("Ctrl+E"))
        self.align_right_action.setShortcut(QKeySequence("Ctrl+R"))
        self.align_justify_action.setShortcut(QKeySequence("Ctrl+J"))

    def update_edit_menu(self) -> None:
        selection_actions = [self.cut_action, self.copy_action, self.bold_action, self.italic_action, self.underline_action,
                             self.strikeout_action, self.align_left_action, self.align_center_action, self.align_right_action, self.align_justify_action]
        for action in selection_actions:
            action.setEnabled(self.text_edit.textCursor().hasSelection())
        self.undo_action.setEnabled(self.text_edit.document().isUndoAvailable())
        self.redo_action.setEnabled(self.text_edit.document().isRedoAvailable())
        self.paste_action.setEnabled(bool(QGuiApplication.clipboard().text()))
        self.select_action.setEnabled(bool(self.text_edit.toPlainText()))
        self.delete_action.setEnabled(bool(self.text_edit.toPlainText()))

    def new_file(self) -> None:
        self.file_manager.new_file(self, self.parent.findChild(QToolBar, "fileToolbar"))
        self.reset_menu_bar()
        self.parent.findChild(QToolBar, "fileToolbar").reset_file_toolbar()
        self.parent.findChild(QToolBar, "textToolbar").reset_text_toolbar()

    def open_file(self) -> None:
        self.file_manager.open_file(self, self.parent.findChild(QToolBar, "fileToolbar"))
        self.parent.findChild(QToolBar, "textToolbar").reset_text_toolbar()

    def save_file(self, file_type: str | None) -> None:
        if file_type is None:
            self.file_manager.save_file()
        else:
            self.file_manager.save_file_as(self, self.parent.findChild(QToolBar, "fileToolbar"), file_type)

    def close_application(self) -> None:
        main_window = self.parent
        main_window.close()

    def reset_menu_bar(self) -> None:
        self.save_action.setDisabled(True)