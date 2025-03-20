import logging

modules = ["start", "random_video", "index", "delete_video", "stats", "quota", "my_plan", "broadcast"]

for module in modules:
    try:
        exec(f"from . import {module}")
    except Exception as e:
        logging.error(f"Failed to load handler {module}: {e}")
