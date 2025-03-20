import os

API_ID = int(os.getenv("API_ID", "27788368"))
API_HASH = os.getenv("API_HASH", "9df7e9ef3d7e4145270045e5e43e1081")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7692429836:AAHyUFP6os1A3Hirisl5TV1O5kArGAlAEuQ")

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://aarshhub:6L1PAPikOnAIHIRA@cluster0.6shiu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DATABASE_NAME = "VideoBotDB"
COLLECTION_NAME = "Videos"

OWNER_ID = int(os.getenv("OWNER_ID", "6860316927"))  # Replace with your Telegram ID
CACHE_DURATION = "300"  # Cache for 5 minutes

AUTO_DELETE_TIME = int(os.getenv("AUTO_DELETE_TIME", "20"))  # 1 day (in seconds)
