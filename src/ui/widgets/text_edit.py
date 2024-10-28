from PyQt6.QtGui import QTextOption
from PyQt6.QtWidgets import QTextEdit, QStatusBar


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
        self.cursorPositionChanged.connect(self.refresh_count_labels)

    def refresh_count_labels(self) -> None:
        lines_count = self.document().blockCount()
        cursor = self.textCursor()
        cursor_line = cursor.blockNumber() + 1
        cursor_char = cursor.columnNumber()
        self.status_bar.update_count_labels(len(self.toPlainText()), lines_count, cursor_line, cursor_char)