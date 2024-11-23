from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QFont, QGuiApplication, QColor
from PyQt6.QtWidgets import QTextEdit, QStatusBar, QMenu, QToolBar

from src.utilities.data_provider import DataProvider


# noinspection PyUnresolvedReferences
class TextEdit(QTextEdit):
    def __init__(self, status_bar: QStatusBar, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("textEdit")
        self.status_bar = status_bar
        self.setStyleSheet("color: #000000; background-color: #FFFFFF;")
        self.setFontFamily("Arial")
        self.setFontPointSize(14)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setTabStopDistance(50)
        self.setAcceptRichText(True)
        self.set_ui_text()
        self.update_context_actions()
        self.cursorPositionChanged.connect(self.refresh_count_labels)
        self.cursorPositionChanged.connect(self.update_context_actions)

    def refresh_count_labels(self) -> None:
        lines_count = self.document().blockCount()
        cursor = self.textCursor()
        cursor_line = cursor.blockNumber() + 1
        cursor_char = cursor.columnNumber()
        self.status_bar.update_count_labels(len(self.toPlainText()), lines_count, cursor_line, cursor_char)

    def contextMenuEvent(self, event) -> None:
        context_menu = QMenu(self)
        context_menu.addAction(self.undo_action)
        context_menu.addAction(self.redo_action)
        context_menu.addAction(self.cut_action)
        context_menu.addAction(self.copy_action)
        context_menu.addAction(self.paste_action)
        context_menu.addSeparator()
        context_menu.addAction(self.select_action)
        context_menu.addAction(self.delete_action)
        context_menu.exec(event.globalPos())

    def set_ui_text(self) -> None:
        ui_text = DataProvider.get_ui_text("textedit")
        self.undo_action = QAction(ui_text.get("undoContext"), self)
        self.undo_action.triggered.connect(self.undo)
        self.redo_action = QAction(ui_text.get("redoContext"), self)
        self.redo_action.triggered.connect(self.redo)
        self.cut_action = QAction(ui_text.get("cutContext"), self)
        self.cut_action.triggered.connect(self.cut)
        self.copy_action = QAction(ui_text.get("copyContext"), self)
        self.copy_action.triggered.connect(self.copy)
        self.paste_action = QAction(ui_text.get("pasteContext"), self)
        self.paste_action.triggered.connect(self.paste)
        self.select_action = QAction(ui_text.get("selectContext"), self)
        self.select_action.triggered.connect(self.selectAll)
        self.delete_action = QAction(ui_text.get("deleteContext"), self)
        self.delete_action.triggered.connect(self.clear)

    def reset_document(self) -> None:
        self.clear()
        self.setFont(QFont("Arial", 14))
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setTextColor(QColor("#000000"))
        self.setTextBackgroundColor(QColor("#FFFFFF"))
        file_toolbar = self.parent().findChild(QToolBar, "fileToolbar")
        text_toolbar = self.parent().findChild(QToolBar, "textToolbar")
        file_toolbar.reset_file_toolbar()
        text_toolbar.reset_text_toolbar()
        self.setFocus()

    def mousePressEvent(self, event) -> None:
        if self.extraSelections():
            self.setExtraSelections([])
        super().mousePressEvent(event)

    def get_text_format(self) -> tuple:
        cursor = self.textCursor()
        char_format = cursor.charFormat()
        if cursor and char_format.isValid():
            is_bold = char_format.fontWeight() == QFont.Weight.Bold
            is_italic = char_format.fontItalic()
            is_underline = char_format.fontUnderline()
            is_strikeout = char_format.fontStrikeOut()
            return is_bold, is_italic, is_underline, is_strikeout
        return False, False, False, False

    def update_context_actions(self) -> None:
        self.undo_action.setEnabled(self.document().isUndoAvailable())
        self.redo_action.setEnabled(self.document().isRedoAvailable())
        self.cut_action.setEnabled(self.textCursor().hasSelection())
        self.copy_action.setEnabled(self.textCursor().hasSelection())
        self.paste_action.setEnabled(bool(QGuiApplication.clipboard().text()))
        self.select_action.setEnabled(bool(self.toPlainText()))
        self.delete_action.setEnabled(bool(self.toPlainText()))