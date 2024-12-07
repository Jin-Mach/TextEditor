from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QFont, QGuiApplication, QMouseEvent
from PyQt6.QtWidgets import QTextEdit, QStatusBar, QMenu, QApplication

from src.utilities.data_provider import DataProvider
from src.utilities.messagebox_manager import MessageboxManager


# noinspection PyUnresolvedReferences
class TextEdit(QTextEdit):
    def __init__(self, status_bar: QStatusBar, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("textEdit")
        self.parent = parent
        self.status_bar = status_bar
        self.setFont(QFont("Arial", 14))
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setTabStopDistance(50)
        self.setAcceptRichText(True)
        self.create_context_menu()
        self.create_connection()
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
        ui_text = DataProvider.get_ui_text("textedit")
        context_menu = QMenu(self)
        actions = [self.undo_action, self.redo_action, self.cut_action, self.copy_action, self.paste_action, self.select_action,
                   self.delete_action]
        for action in actions:
            if action == self.select_action:
                context_menu.addSeparator()
                action.setText(ui_text.get(action.objectName()))
                context_menu.addAction(action)
            action.setText(ui_text.get(action.objectName()))
            context_menu.addAction(action)
        context_menu.exec(event.globalPos())

    def create_context_menu(self) -> None:
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
        self.select_action.setObjectName("select")
        self.delete_action = QAction(self)
        self.delete_action.setObjectName("delete")

    def create_connection(self) -> None:
        self.undo_action.triggered.connect(self.undo)
        self.redo_action.triggered.connect(self.redo)
        self.cut_action.triggered.connect(self.cut)
        self.copy_action.triggered.connect(self.copy)
        self.paste_action.triggered.connect(self.custom_paste)
        self.select_action.triggered.connect(self.selectAll)
        self.delete_action.triggered.connect(self.clear_text_edit)

    def reset_text_edit(self) -> None:
        self.clear()
        self.setFont(QFont("Arial", 14))
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setFocus()

    def mousePressEvent(self, event: QMouseEvent) -> None:
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

    def custom_paste(self) -> None:
        clipboard = QApplication.clipboard()
        self.insertPlainText(clipboard.text())

    def clear_text_edit(self) -> None:
        try:
            messagebox_manager = MessageboxManager(self.parent)
            result = messagebox_manager.document_contains_text()
            if result == "continue":
                self.clear()
            self.setFocus()
        except Exception as e:
            ExceptionManager.exception_handler(e)