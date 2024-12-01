import pathlib

from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QToolBar
from PyQt6.QtGui import QAction, QIcon

from src.utilities.data_provider import DataProvider


# noinspection PyUnresolvedReferences
class TrayIcon(QSystemTrayIcon):
    icons_path = pathlib.Path(__file__).parent.parent.joinpath("icons")
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setIcon(QIcon(str(self.icons_path.joinpath("applicationIcon.png"))))
        self.create_gui()

    def create_gui(self):
        ui_text = DataProvider().get_ui_text("trayicon")
        tray_menu = QMenu()
        self.new_file_action = QAction(ui_text.get("newFile"), self)
        self.new_file_action.setIcon(QIcon(str(self.icons_path.joinpath("file_icons", "newFile.png"))))
        self.open_file_action = QAction(ui_text.get("openFile"), self)
        self.open_file_action.setIcon(QIcon(str(self.icons_path.joinpath("file_icons", "openFile"))))
        self.quit_action = QAction(ui_text.get("closeApplication"), self)
        self.quit_action.setIcon(QIcon(str(self.icons_path.joinpath("closeApplication.png"))))
        tray_menu.addAction(self.new_file_action)
        tray_menu.addAction(self.open_file_action)
        tray_menu.addSeparator()
        tray_menu.addAction(self.quit_action)
        self.setContextMenu(tray_menu)
        self.show()

    def create_connection(self) -> None:
        self.new_file_action.triggered.connect(self.parent().findChild(QToolBar, "fileToolbar").new_file)
        self.open_file_action.triggered.connect(self.parent().findChild(QToolBar, "fileToolbar").open_file)
        self.quit_action.triggered.connect(self.close_app)

    def close_app(self) -> None:
        self.parent().close()