import logging
import os
from logging.handlers import RotatingFileHandler


def get_logger(name: str) -> logging.Logger:
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_FILE = os.getenv("LOG_FILE", "app.log")

    FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    TIME_FORMAT = "%d-%m-%Y %H:%M:%S"

    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    # Evitar handlers duplicados
    if logger.handlers:
        return logger

    formatter = logging.Formatter(FORMAT, TIME_FORMAT)

    # Consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Archivo con rotación
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=10 * 1024 * 1024,
        backupCount=3,
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Evita que los logs se dupliquen hacia el root
    logger.propagate = False

    return logger
