from .db import db

video_collection = db["Videos"]
quota_collection = db["Quota"]

def get_random_video():
    return video_collection.aggregate([{"$sample": {"size": 1}}]).next()

def index_video(file_id):
    if video_collection.find_one({"file_id": file_id}):
        return "This video is already indexed!"
    video_collection.insert_one({"file_id": file_id})
    return "Video indexed successfully!"

def delete_video(file_id):
    result = video_collection.delete_one({"file_id": file_id})
    return "Video deleted!" if result.deleted_count else "Video not found!"

def get_video_count():
    return video_collection.count_documents({})

def check_quota(user_id):
    user_quota = quota_collection.find_one({"user_id": user_id})
    return user_quota["remaining"] if user_quota else 10  # Default 10

def reset_quota():
    quota_collection.update_many({}, {"$set": {"remaining": 10}})
