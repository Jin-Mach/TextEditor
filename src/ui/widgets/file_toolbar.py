from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QToolBar


class FileToolbar(QToolBar):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("fileToolbar")
        self.setAllowedAreas(Qt.ToolBarArea.TopToolBarArea)
        self.setOrientation(Qt.Orientation.Horizontal)
        self.setFloatable(False)
        self.setMovable(False)