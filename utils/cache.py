import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

cache = {}

def get_cached(key):
    """Retrieve cached value if it exists and hasn't expired."""
    try:
        if key in cache and cache[key]['expires'] > time.time():
            return cache[key]['value']
        return None
    except Exception as e:
        logger.error(f"❌ Error retrieving cache for key '{key}': {e}")
        return None  # Return None in case of failure

def set_cache(key, value, duration):
    """Store a value in the cache with an expiration time."""
    try:
        cache[key] = {"value": value, "expires": time.time() + duration}
        logger.info(f"✅ Cached key '{key}' for {duration} seconds.")
    except Exception as e:
        logger.error(f"❌ Error setting cache for key '{key}': {e}")

class Cache:
    """Simple in-memory cache system with error handling."""
    
    def __init__(self):
        self.storage = {}

    def set(self, key, value):
        """Store a value in the cache."""
        try:
            self.storage[key] = value
            logger.info(f"✅ Cached key '{key}' successfully.")
        except Exception as e:
            logger.error(f"❌ Error setting cache key '{key}': {e}")

    def get(self, key):
        """Retrieve a value from the cache."""
        try:
            return self.storage.get(key, None)
        except Exception as e:
            logger.error(f"❌ Error retrieving cache key '{key}': {e}")
            return None

    def delete(self, key):
        """Remove a key from the cache."""
        try:
            if key in self.storage:
                del self.storage[key]
                logger.info(f"🗑️ Deleted cache key '{key}'.")
        except Exception as e:
            logger.error(f"❌ Error deleting cache key '{key}': {e}")

    def clear(self):
        """Clear all cache data."""
        try:
            self.storage.clear()
            logger.info("🚀 Cache cleared successfully.")
        except Exception as e:
            logger.error(f"❌ Error clearing cache: {e}")
