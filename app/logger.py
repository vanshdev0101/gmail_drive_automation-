import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

def _create_handler(log_file, level):
    handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=5
    )
    formatter = logging.Formatter(LOG_FORMAT)
    handler.setFormatter(formatter)
    handler.setLevel(level)
    return handler

def get_app_logger():
    logger = logging.getLogger("app")
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    Path("logs").mkdir(exist_ok=True)

    handler = _create_handler("logs/app.log", logging.INFO)
    logger.addHandler(handler)

    return logger

def get_audit_logger():
    logger = logging.getLogger("audit")
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    Path("logs").mkdir(exist_ok=True)

    handler = _create_handler("logs/audit.log", logging.INFO)
    logger.addHandler(handler)

    return logger
