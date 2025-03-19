import time

cache = {}

def get_cached(key):
    if key in cache and cache[key]['expires'] > time.time():
        return cache[key]['value']
    return None

def set_cache(key, value, duration):
    cache[key] = {"value": value, "expires": time.time() + duration}


class Cache:
    """Simple in-memory cache system"""
    
    def __init__(self):
        self.storage = {}

    def set(self, key, value):
        """Store a value in the cache."""
        self.storage[key] = value

    def get(self, key):
        """Retrieve a value from the cache."""
        return self.storage.get(key, None)

    def delete(self, key):
        """Remove a key from the cache."""
        if key in self.storage:
            del self.storage[key]

    def clear(self):
        """Clear all cache data."""
        self.storage.clear()
