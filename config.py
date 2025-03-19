import os

API_ID = int(os.getenv("API_ID", "27788368"))
API_HASH = os.getenv("API_HASH", "9df7e9ef3d7e4145270045e5e43e1081")
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")

MONGO_URI = os.getenv("MONGO_URI", "YOUR_MONGO_URI")
DATABASE_NAME = "VideoBotDB"
COLLECTION_NAME = "Videos"

OWNER_ID = int(os.getenv("OWNER_ID", "6860316927"))  # Replace with your Telegram ID
CACHE_DURATION = "300"  # Cache for 5 minutes

AUTO_DELETE_TIME = int(os.getenv("AUTO_DELETE_TIME", "20"))  # 1 day (in seconds)
