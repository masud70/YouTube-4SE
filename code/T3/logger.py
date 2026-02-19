import logging

def get_logger():
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        filename="logs/gptoss.txt",
        filemode='w',
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )
    return logger