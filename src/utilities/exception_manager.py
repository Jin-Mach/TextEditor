from src.utilities.logging_manager import setup_logger
from src.utilities.messagebox_manager import MessageboxManager


class ExceptionManager:

    @staticmethod
    def exception_handler(exception: Exception) -> None:
        logger = setup_logger()
        logger.error("An error occurred: %s", exception, exc_info=True)
        messagebox_manager = MessageboxManager()
        messagebox_manager.show_error_message(exception)