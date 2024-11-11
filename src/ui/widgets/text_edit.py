from PyQt6.QtGui import QTextOption, QAction, QFont
from PyQt6.QtWidgets import QTextEdit, QStatusBar, QMenu, QToolBar

from src.utilities.data_provider import DataProvider


# noinspection PyUnresolvedReferences
class TextEdit(QTextEdit):
    def __init__(self, status_bar: QStatusBar, parent=None) -> None:
        super().__init__(parent)
        self.status_bar = status_bar
        self.setObjectName("textEdit")
        self.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.setTabStopDistance(50)
        self.setAcceptRichText(True)
        self.set_ui_text()
        self.cursorPositionChanged.connect(self.refresh_count_labels)

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
        self.redo_action = QAction(ui_text.get("redoContext"), self)
        self.cut_action = QAction(ui_text.get("cutContext"), self)
        self.copy_action = QAction(ui_text.get("copyContext"), self)
        self.paste_action = QAction(ui_text.get("pasteContext"), self)
        self.select_action = QAction(ui_text.get("selectContext"), self)
        self.delete_action = QAction(ui_text.get("deleteContext"), self)

    def reset_text_edit(self) -> None:
        self.clear()
        self.setFont(QFont("Arial", 14))
        self.setFocus()
        text_toolbars = self.parent().findChildren(QToolBar)
        for toolbar in text_toolbars:
            if toolbar.objectName() == "fileToolbar":
                toolbar.save_button.setDisabled(True)
            elif toolbar.objectName() == "textToolbar":
                toolbar.font_family_combobox.setCurrentText("Arial")
                toolbar.font_size_combobox.setCurrentText("14")

    def mousePressEvent(self, event) -> None:
        if self.extraSelections():
            self.setExtraSelections([])
        super().mousePressEvent(event)