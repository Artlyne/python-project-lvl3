import logging

LOG_FORMAT = '%(asctime)s - [%(levelname)s] - %(filename)s - ' \
             '%(funcName)s(%(lineno)d) - %(message)s'


def get_logger(name):
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    logger = logging.getLogger(name)
    return logger
