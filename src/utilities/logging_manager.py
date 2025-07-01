import logging
from logging.handlers import RotatingFileHandler
import pathlib

logging_file = pathlib.Path.joinpath(pathlib.Path(__file__).parent.parent, "data", "log_files", "texteditor_errors.log")
logging_file.parent.mkdir(parents=True, exist_ok=True)

def setup_logger() -> logging.Logger:
    formater = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler = RotatingFileHandler(logging_file, mode="a", encoding="utf-8", maxBytes=5 * 1024 * 1024, backupCount=1)
    handler.setFormatter(formater)
    logger = logging.getLogger(pathlib.Path(__name__).name)
    logger.setLevel(logging.WARNING)

    if not logger.hasHandlers():
        logger.addHandler(handler)
    return logger