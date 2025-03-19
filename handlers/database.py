import motor.motor_asyncio
from config import MONGO_URI, DATABASE_NAME

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client[DATABASE_NAME]
users = db.users
videos = db.videos

async def init_db():
    await db.command("ping")

async def get_total_users():
    return await users.count_documents({})

async def get_total_videos():
    return await videos.count_documents({})

async def add_video(file_id):
    if await videos.find_one({"file_id": file_id}):
        return False
    await videos.insert_one({"file_id": file_id})
    return True

async def delete_video(file_id):
    result = await videos.delete_one({"file_id": file_id})
    return result.deleted_count > 0

async def get_random_video():
    video = await videos.aggregate([{ "$sample": { "size": 1 } }]).to_list(length=1)
    return video[0] if video else None
