from .db import db

# Collections
user_collection = db["Users"]
video_collection = db["Videos"]
quota_collection = db["Quota"]

# ✅ Get User Plan
def get_user_plan(user_id):
    user = user_collection.find_one({"user_id": user_id}, {"plan": 1})
    return user["plan"] if user else "Free"

# ✅ Get All Users (For Broadcasting)
def get_all_users():
    return list(user_collection.distinct("user_id"))

# ✅ Get a Random Video
def get_random_video():
    video = video_collection.aggregate([{"$sample": {"size": 1}}])
    return next(video, None)  

# ✅ Index a Video
def index_video(file_id):
    if video_collection.find_one({"file_id": file_id}):
        return "⚠️ This video is already indexed!"
    
    video_collection.insert_one({"file_id": file_id})
    return "✅ Video indexed successfully!"

# ✅ Delete a Video
def delete_video(file_id):
    result = video_collection.delete_one({"file_id": file_id})
    return "✅ Video deleted!" if result.deleted_count else "⚠️ Video not found!"

# ✅ Get Total Video Count
def get_video_count():
    return video_collection.count_documents({})

# ✅ Check User Quota
def check_quota(user_id):
    user_quota = quota_collection.find_one({"user_id": user_id}, {"remaining": 1})
    return user_quota["remaining"] if user_quota else 10  

# ✅ Reset All User Quotas
def reset_quota():
    quota_collection.update_many({}, {"$set": {"remaining": 10}})
