import logging
import os

class LoggerException(Exception):
    pass


def get_logger(logger_name, log_file, level=logging.INFO):
    if not os.access(log_file, os.W_OK):
       raise LoggerException("log file is not writeable")

    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(levelname)-8s [%(asctime)s] %(message)s')
    file_handler = logging.FileHandler(log_file, mode='a')
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
