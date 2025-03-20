import logging
import os

def setup_logger():
    """Setup logger for the bot with both console and file logging."""
    try:
        logger = logging.getLogger("BotLogger")
        logger.setLevel(logging.INFO)

        # Log format
        log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_format)
        logger.addHandler(console_handler)

        # File Handler (logs stored in logs/bot.log)
        log_dir = "logs"
        log_file = os.path.join(log_dir, "bot.log")

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)  # Create log directory if not exists

        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)

        logger.info("✅ Logger initialized successfully.")
        return logger

    except Exception as e:
        print(f"❌ Error setting up logger: {e}")
        return None  # Return None to avoid crashes

logger = setup_logger()
