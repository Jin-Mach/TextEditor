import pathlib

from PyQt6.QtGui import QPageLayout, QPageSize
from PyQt6.QtPrintSupport import QPrinter
from PyQt6.QtCore import QMarginsF
from PyQt6.QtWidgets import QToolBar, QMenuBar, QSystemTrayIcon

from src.ui.widgets.text_toolbar import TextToolbar
from src.ui.widgets.text_edit import TextEdit
from src.utilities.data_provider import DataProvider
from src.utilities.exception_manager import ExceptionManager
from src.ui.dialogs.messagebox_manager import MessageboxManager
from src.ui.dialogs.file_dialog_manager import FileDialogManager


# noinspection PyUnresolvedReferences
class FileManager:
    def __init__(self, language_code: str, text_edit: TextEdit, tray_icon: QSystemTrayIcon, parent=None) -> None:
        self.language_code = language_code
        self.parent = parent
        self.text_edit = text_edit
        self.tray_icon = tray_icon
        self.last_file_path = ""
        self.text_toolbar = TextToolbar(self.language_code, self.text_edit, self.parent)
        self.messagebox_manager = MessageboxManager(self.parent)
        self.dialog_manager = FileDialogManager(self.parent)
        self.dialog_ui_text = DataProvider.get_ui_text("dialog", self.language_code)
        self.messagebox_ui_text = DataProvider.get_ui_text("messagebox", self.language_code)
        self.tray_icon_ui_text = DataProvider.get_ui_text("trayicon", self.language_code)

    def new_file(self, menu_bar: QMenuBar, file_toolbar: QToolBar) -> None:
        try:
            if self.text_edit.toPlainText().strip():
                result = self.messagebox_manager.show_save_question_message()
                if result == "dontSave":
                    self.text_edit.reset_text_edit()
                    self.last_file_path = ""
                elif result == "saveAs":
                    self.save_file_as(menu_bar, file_toolbar, ".txt")
                    self.text_edit.reset_text_edit()
                elif result == "cancel":
                    self.text_edit.setFocus()
            self.text_edit.document().setModified(False)
        except Exception as e:
            ExceptionManager.exception_handler(e)

    def open_file(self, menu_bar: QMenuBar, file_toolbar: QToolBar) -> None:
        try:
            if not self.text_edit.document().isModified() or self.text_edit.document().isEmpty():
                selected_file = self.dialog_manager.open_file_dialog()
                if selected_file and pathlib.Path(selected_file).exists():
                    self.text_edit.reset_text_edit()
                    self.load_file_content(selected_file)
                    self.last_file_path = selected_file
                else:
                    self.last_file_path = ""
            else:
                result = self.messagebox_manager.show_save_question_message()
                if result == "dontSave":
                    selected_file = str(self.dialog_manager.open_file_dialog())
                    if selected_file and pathlib.Path(selected_file).exists():
                        self.text_edit.reset_text_edit()
                        self.load_file_content(selected_file)
                elif result == "saveAs":
                    self.save_file_as(menu_bar, file_toolbar, ".txt")
                elif result == "cancel":
                    self.text_edit.setFocus()
            menu_bar.save_action.setDisabled(not bool(self.last_file_path))
            file_toolbar.save_button.setDisabled(not bool(self.last_file_path))
            self.text_edit.setFocus()
        except Exception as e:
            ExceptionManager.exception_handler(e)

    def save_file_as(self, menu_bar: QMenuBar, file_toolbar: QToolBar,  file_type: str) -> bool | None:
        try:
            if not self.text_edit.toPlainText():
                self.messagebox_manager.show_empty_document_message(self.text_edit, self.messagebox_ui_text.get("emptytextText"))
                return False
            else:
                file_path = self.dialog_manager.save_document_dialog(f"{self.dialog_ui_text.get("filefilterName")} (*{file_type})")
                if file_path:
                    self.save_document(file_path, file_type)
                    self.last_file_path = file_path
                    menu_bar.save_action.setDisabled(False)
                    file_toolbar.save_button.setDisabled(False)
                self.text_edit.setFocus()
        except Exception as e:
            ExceptionManager.exception_handler(e)
            return None

    def save_file(self) -> None:
        try:
            if not self.text_edit.toPlainText():
                self.messagebox_manager.show_empty_document_message(self.text_edit, self.messagebox_ui_text.get("emptytextText"))
            else:
                file_type = pathlib.Path(self.last_file_path).suffix
                self.save_document(self.last_file_path, file_type)
        except Exception as e:
            ExceptionManager.exception_handler(e)

    def load_file_content(self, file_path: str) -> None:
        try:
            if not file_path or not pathlib.Path(file_path).exists():
                self.text_edit.setFocus()
                self.tray_icon.showMessage(self.tray_icon_ui_text.get("errorTitle"), self.tray_icon_ui_text.get("erroropenText"))
                return
            if file_path.endswith(".html"):
                with open(file_path, "r", encoding="utf-8") as file:
                    self.text_edit.setHtml(file.read())
            elif file_path.endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as file:
                    self.text_edit.setPlainText(file.read())
            self.last_file_path = file_path
            cursor = self.text_edit.textCursor()
            cursor.movePosition(cursor.MoveOperation.End)
            self.text_edit.setTextCursor(cursor)
            self.text_edit.setFocus()
            self.text_edit.document().setModified(False)
        except Exception as e:
            ExceptionManager.exception_handler(e)

    def save_document(self, file_path: str, file_type: str) -> None:
        try:
            if file_type == ".txt":
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.text_edit.toPlainText())
            elif file_type == ".html":
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.text_edit.toHtml())
            elif file_type == ".pdf":
                printer = QPrinter(QPrinter.PrinterMode.HighResolution)
                printer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
                margins = QMarginsF(10, 10, 10, 10)
                printer.setPageMargins(margins, QPageLayout.Unit.Millimeter)
                printer.setColorMode(QPrinter.ColorMode.Color)
                printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
                printer.setOutputFileName(file_path)
                self.text_edit.document().print(printer)
            if pathlib.Path(file_path).exists():
                self.tray_icon.showMessage(self.tray_icon_ui_text.get("saveTitle"), self.tray_icon_ui_text.get("saveText"))
            else:
                self.tray_icon.showMessage(self.tray_icon_ui_text.get("errorTitle"), self.tray_icon_ui_text.get("errorsaveText"))
            self.text_edit.document().setModified(False)
            self.text_edit.setFocus()
        except Exception as e:
            ExceptionManager.exception_handler(e)