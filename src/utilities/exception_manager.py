from src.utilities.logging_manager import setup_logger


class ExceptionManager:

    @staticmethod
    def exception_handler(exception: Exception) -> None:
        from src.utilities.messagebox_manager import MessageboxManager
        logger = setup_logger()
        logger.error("An error occurred: %s", exception, exc_info=True)
        messagebox_manager = MessageboxManager()
        messagebox_manager.show_error_message(exception)