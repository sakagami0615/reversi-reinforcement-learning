from logging import getLogger, Logger, StreamHandler, Formatter, DEBUG


def create_logger(name, level: int = DEBUG) -> Logger:
    logger = getLogger(name)
    logger.setLevel(DEBUG)

    st_handler = StreamHandler()
    st_handler.setLevel(DEBUG)
    st_handler.setFormatter(Formatter("[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d] %(message)s"))
    logger.addHandler(st_handler)
    return logger
