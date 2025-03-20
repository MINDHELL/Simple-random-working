try:
    from .helpers import format_time, human_readable_size
    from .cache import Cache
    from .logger import setup_logger

    # Initialize logger
    logger = setup_logger()
    logger.info("✅ Utilities module loaded successfully!")

except ImportError as e:
    print(f"❌ Import Error in utils: {e}")
    raise  # Raise the error to prevent silent failures
except Exception as e:
    print(f"❌ Unexpected Error in utils: {e}")
    raise  # Raise any unexpected errors
