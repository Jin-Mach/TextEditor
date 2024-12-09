from PyQt6.QtCore import QMarginsF, QTranslator, QLocale, QLibraryInfo
from PyQt6.QtGui import QPageSize, QPageLayout
from PyQt6.QtPrintSupport import QPrinter, QPrintPreviewDialog, QPrintDialog
from PyQt6.QtWidgets import QApplication

from src.ui.widgets.text_edit import TextEdit
from src.utilities.data_provider import DataProvider
from src.utilities.exception_manager import ExceptionManager
from src.utilities.messagebox_manager import MessageboxManager


class Printmanager:
    def __init__(self, language_code: str, text_edit: TextEdit, parent=None) -> None:
        self.language_code = language_code
        self.text_edit = text_edit
        self.parent = parent
        self.ui_text = DataProvider.get_ui_text("messagebox", self.language_code)

    def show_print_preview(self) -> None:
        try:
            if self.text_edit.toPlainText():
                translator = QTranslator()
                locale = QLocale.system().name()
                translations_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
                if translator.load(f"qtbase_{locale}", translations_path):
                    QApplication.instance().installTranslator(translator)
                printer = QPrinter(QPrinter.PrinterMode.HighResolution)
                printer.setColorMode(QPrinter.ColorMode.Color)
                printer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
                margins = QMarginsF(10, 10, 10, 10)
                printer.setPageMargins(margins, QPageLayout.Unit.Millimeter)
                printer.setPageOrientation(QPageLayout.Orientation.Portrait)
                preview_dialog = QPrintPreviewDialog(printer, self.parent)
                preview_dialog.paintRequested.connect(self.render_document)
                preview_dialog.exec()
                if not translator.isEmpty():
                    QApplication.instance().removeTranslator(translator)
            else:
                message_box = MessageboxManager(self.parent)
                message_box.show_empty_document_message(self.text_edit, self.ui_text.get("emptyPreview"))
        except Exception as e:
            ExceptionManager.exception_handler(e)

    def render_document(self, printer) -> None:
        document = self.text_edit.document()
        document.print(printer)

    def print_document(self) -> None:
        try:
            if self.text_edit.toPlainText():
                printer = QPrinter(QPrinter.PrinterMode.HighResolution)
                printer.setColorMode(QPrinter.ColorMode.Color)
                printer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
                margins = QMarginsF(10, 10, 10, 10)
                printer.setPageMargins(margins, QPageLayout.Unit.Millimeter)
                printer.setPageOrientation(QPageLayout.Orientation.Portrait)
                print_dialog = QPrintDialog(printer, self.parent)
                if print_dialog.exec() == QPrintDialog.DialogCode.Accepted:
                    document = self.text_edit.document()
                    document.print(printer)
            else:
                message_box = MessageboxManager(self.parent)
                message_box.show_empty_document_message(self.text_edit, self.ui_text.get("emptyPrint"))
        except Exception as e:
            ExceptionManager.exception_handler(e)