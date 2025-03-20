from .db import db

video_collection = db["Videos"]
quota_collection = db["Quota"]

# ✅ Get a random video
async def get_random_video():
    video = await video_collection.aggregate([{"$sample": {"size": 1}}]).to_list(1)
    return video[0] if video else None

# ✅ Index a new video
async def index_video(file_id):
    if await video_collection.find_one({"file_id": file_id}):
        return "⚠️ This video is already indexed!"
    await video_collection.insert_one({"file_id": file_id})
    return "✅ Video indexed successfully!"

# ✅ Delete a video
async def delete_video(file_id):
    result = await video_collection.delete_one({"file_id": file_id})
    return "✅ Video deleted!" if result.deleted_count else "⚠️ Video not found!"

# ✅ Get total video count
async def get_video_count():
    return await video_collection.count_documents({})

# ✅ Check user's quota
async def check_quota(user_id):
    user_quota = await quota_collection.find_one({"user_id": user_id}, {"_id": 0, "remaining": 1})
    return user_quota["remaining"] if user_quota else 10  # Default 10 videos per day

# ✅ Decrease user's quota
async def increment_video_usage(user_id):
    await quota_collection.update_one(
        {"user_id": user_id}, {"$inc": {"remaining": -1}}, upsert=True
    )

# ✅ Reset all user quotas
async def reset_quota():
    await quota_collection.update_many({}, {"$set": {"remaining": 10}})
