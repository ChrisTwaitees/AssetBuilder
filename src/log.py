import os
import logging


def init_logging():
    logger_name = "AssetBuilderLoger"
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(' %(levelname)s - %(message)s')

    file_handler = logging.FileHandler(os.path.join(logs_dir, "AssetBuilderLoger.log"), 'w+')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


LOG = init_logging()
