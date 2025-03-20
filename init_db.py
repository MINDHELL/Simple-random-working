from pymongo import MongoClient
from config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
video_collection = db[COLLECTION_NAME]

# Ensure unique index to prevent duplicate videos
video_collection.create_index("file_id", unique=True)

print("Database initialized successfully!")
