from src.utilities.logging_manager import setup_logger
from src.utilities.messagebox_manager import MessageboxManager


class ExceptionManager:

    @staticmethod
    def exception_handler(exception: Exception) -> None:
        setup_logger().error(str(exception))
        messagebox_manager = MessageboxManager()
        messagebox_manager.show_error_message(exception)