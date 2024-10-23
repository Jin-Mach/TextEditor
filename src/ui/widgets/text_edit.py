from PyQt6.QtGui import QFont, QTextOption
from PyQt6.QtWidgets import QTextEdit


class TextEdit(QTextEdit):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("textEdit")
        self.setFont(QFont("Arial", 13))
        self.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.setTabStopDistance(50)
        self.setAcceptRichText(True)