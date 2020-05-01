import logging

logging.basicConfig(filename='dev.log',
                    filemode='w',
                    level=logging.DEBUG,
                    # format='%(levelname)s %(asctime)s %(name)s %(message)s',
                    format='%(asctime)s: [%(levelname)s] - [%(name)s] - %(message)s')


def create_logger(name=__name__):
    logger = logging.getLogger(name)
    return logger
