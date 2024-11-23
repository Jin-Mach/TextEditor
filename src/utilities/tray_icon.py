import pathlib

from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QAction, QIcon

from src.utilities.data_provider import DataProvider


# noinspection PyUnresolvedReferences
class TrayIcon(QSystemTrayIcon):
    def __init__(self, file_manager=None, parent=None) -> None:
        super().__init__(parent)
        self.file_manager = file_manager
        self.setIcon(parent.style().standardIcon(parent.style().StandardPixmap.SP_ComputerIcon))
        self.create_gui()
        self.create_connection()

    def create_gui(self):
        ui_text = DataProvider().get_ui_text("trayicon")
        icons_path = pathlib.Path(__file__).parent.parent.joinpath("icons")
        tray_menu = QMenu()
        self.new_file_action = QAction(ui_text.get("newFile"), self)
        self.new_file_action.setIcon(QIcon(str(icons_path.joinpath("file_icons", "newFile.png"))))
        self.open_file_action = QAction(ui_text.get("openFile"), self)
        self.open_file_action.setIcon(QIcon(str(icons_path.joinpath("file_icons", "openFile"))))
        self.quit_action = QAction(ui_text.get("closeApplication"), self)
        self.quit_action.setIcon(QIcon(str(icons_path.joinpath("closeApplication.png"))))
        tray_menu.addAction(self.new_file_action)
        tray_menu.addAction(self.open_file_action)
        tray_menu.addSeparator()
        tray_menu.addAction(self.quit_action)
        self.setContextMenu(tray_menu)
        self.show()

    def create_connection(self) -> None:
        self.new_file_action.triggered.connect(self.file_manager.new_file)
        self.open_file_action.triggered.connect(self.file_manager.open_file)
        self.quit_action.triggered.connect(self.close_app)

    def close_app(self) -> None:
        main_window = self.parent().parent
        main_window.close()