from .db import db

# Collections
user_collection = db["Users"]  
video_collection = db["Videos"]
quota_collection = db["Quota"]

# ✅ Function to Get User Plan
def get_user_plan(user_id):
    user = user_collection.find_one({"user_id": user_id})
    return user.get("plan", "Free") if user else "Free"  # Default to "Free"

# ✅ Function to Get a Random Video
def get_random_video():
    return video_collection.aggregate([{"$sample": {"size": 1}}]).next()

# ✅ Function to Index a Video
def index_video(file_id):
    if video_collection.find_one({"file_id": file_id}):
        return "This video is already indexed!"
    video_collection.insert_one({"file_id": file_id})
    return "Video indexed successfully!"

# ✅ Function to Delete a Video
def delete_video(file_id):
    result = video_collection.delete_one({"file_id": file_id})
    return "Video deleted!" if result.deleted_count else "Video not found!"

# ✅ Function to Get Total Video Count
def get_video_count():
    return video_collection.count_documents({})

# ✅ Function to Check User Quota
def check_quota(user_id):
    user_quota = quota_collection.find_one({"user_id": user_id})
    return user_quota["remaining"] if user_quota else 10  # Default 10

# ✅ Function to Reset All User Quotas
def reset_quota():
    quota_collection.update_many({}, {"$set": {"remaining": 10}})
