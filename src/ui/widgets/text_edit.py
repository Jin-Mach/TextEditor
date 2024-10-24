from PyQt6.QtGui import QTextOption
from PyQt6.QtWidgets import QTextEdit


class TextEdit(QTextEdit):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("textEdit")
        self.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.setTabStopDistance(50)
        self.setAcceptRichText(True)