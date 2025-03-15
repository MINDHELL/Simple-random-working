import os
import logging
import random
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import PeerIdInvalid, FloodWait
from pymongo import MongoClient

# 🔰 Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔰 Environment Variables
API_ID = "27788368"
API_HASH = "9df7e9ef3d7e4145270045e5e43e1081"
BOT_TOKEN = "7725707727:AAFtx6Sy-q6GgB9eaPoN2-oYPx2D6hjnc1g"
MONGO_URL = "mongodb+srv://aarshhub:6L1PAPikOnAIHIRA@cluster0.6shiu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
CHANNEL_ID = "-1002492623985"  # Make sure this is correct
OWNER_ID = "6860316927"  # Your Telegram ID

# 🔰 Initialize Bot & Database
bot = Client("video_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
mongo = MongoClient(MONGO_URL)
db = mongo["VideoBot"]
collection = db["videos"]

# 🔹 Fix /index Command
@bot.on_message(filters.command("index") & filters.user(OWNER_ID))
async def index_videos(client, message):
    await message.reply_text("🔄 Starting video indexing...")

    indexed_count = 0
    try:
        async for msg in client.get_chat_history(CHANNEL_ID, limit=5000):
            if msg.video:
                collection.update_one(
                    {"message_id": msg.id},
                    {"$set": {"message_id": msg.id}}, 
                    upsert=True
                )
                indexed_count += 1
                await asyncio.sleep(0.2)  # Prevent rate limit issues

        await message.reply_text(f"✅ Indexing complete! {indexed_count} videos added.")
        logger.info(f"✅ Indexed {indexed_count} videos.")

    except PeerIdInvalid:
        await message.reply_text("❌ Bot does not have access to the channel! Make sure it's an admin.")
        logger.error("❌ Bot does not have access to the channel!")

    except Exception as e:
        await message.reply_text("❌ Error indexing videos.")
        logger.error(f"❌ Indexing error: {e}")

# 🔹 Fix /files Command
@bot.on_message(filters.command("files") & filters.user(OWNER_ID))
async def get_file_count(client, message):
    try:
        count = collection.count_documents({})
        await message.reply_text(f"📂 Total indexed videos: {count}")
    except Exception as e:
        await message.reply_text("❌ Error getting file count.")
        logger.error(f"❌ File count error: {e}")

# 🔹 Fix Repeating Video Issue
@bot.on_message(filters.command("random"))
async def send_random_video(client, message):
    try:
        video_docs = list(collection.find({}))
        if not video_docs:
            await message.reply_text("⚠ No videos available. Use /index first!")
            return

        random.shuffle(video_docs)  # Ensure random selection
        selected_videos = random.sample(video_docs, min(5, len(video_docs)))  # Select random 5 videos

        for video in selected_videos:
            message_id = video["message_id"]
            try:
                await client.copy_message(
                    chat_id=message.chat.id,
                    from_chat_id=CHANNEL_ID,
                    message_id=message_id
                )
                await asyncio.sleep(1)  # Prevent rate limits
            except FloodWait as e:
                logger.warning(f"⏳ FloodWait: Sleeping for {e.value} seconds...")
                await asyncio.sleep(e.value)
            except Exception as e:
                logger.error(f"⚠ Error fetching video: {e}")

    except Exception as e:
        logger.error(f"❌ Error sending video: {e}")
        await message.reply_text("❌ Error: Could not fetch a video.")

# 🔹 Start Bot
if __name__ == "__main__":
    bot.run()
