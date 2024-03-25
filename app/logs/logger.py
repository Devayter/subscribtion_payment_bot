import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


BASE_DIR = Path(__file__).parent

DT_LOGS_FORMAT = '%d.%m.%Y %H:%M:%S'
LOG_FORMAT = '"%(asctime)s - %(name)s - [%(levelname)s] - %(message)s"'


def configure_logging(name):
    log_file = BASE_DIR / (name + '.log')
    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=10 ** 6, backupCount=5, encoding='utf-8'
    )
    logging.basicConfig(
        datefmt=DT_LOGS_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=[rotating_handler]
    )
