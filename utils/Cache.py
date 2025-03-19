import time

cache = {}

def get_cached(key):
    if key in cache and cache[key]['expires'] > time.time():
        return cache[key]['value']
    return None

def set_cache(key, value, duration):
    cache[key] = {"value": value, "expires": time.time() + duration}
