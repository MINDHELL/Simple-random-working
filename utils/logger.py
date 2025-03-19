import logging

def setup_logger():
    """Setup logger for the bot."""
    logger = logging.getLogger("BotLogger")
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    logger.addHandler(handler)
    return logger

logger = setup_logger()
