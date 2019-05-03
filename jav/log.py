import logging

logging.basicConfig(filename='dev.log',
                    filemode='w',
                    level=logging.DEBUG,
                    format='%(asctime)s, %(name)s, %(levelname)s: %(message)s')


def create_logger(name=__name__):
    logger = logging.getLogger(name)
    return logger
