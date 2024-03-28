import logging


def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    handler = logging.StreamHandler()
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
