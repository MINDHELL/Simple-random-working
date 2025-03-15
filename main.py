import os
import logging
import random
import asyncio
from pyrogram import Client, filters
from pymongo import MongoClient
from pyrogram.errors import FloodWait

# 🔰 Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔰 Environment Variables
API_ID = "27788368"
API_HASH = "9df7e9ef3d7e4145270045e5e43e1081"
BOT_TOKEN = "7725707727:AAFtx6Sy-q6GgB9eaPoN2-oYPx2D6hjnc1g"
MONGO_URL = "mongodb+srv://aarshhub:6L1PAPikOnAIHIRA@cluster0.6shiu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
CHANNEL_ID = "-1002492623985"  # Your channel ID
OWNER_ID = "6860316927"  # Your Telegram ID

# 🔰 Initialize Bot & Database
bot = Client("video_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
mongo = MongoClient(MONGO_URL)
db = mongo["VideoBot"]
collection = db["videos"]

# 🔹 ✅ Auto-Index Videos from Channel
@bot.on_message(filters.video & filters.chat(CHANNEL_ID))
async def auto_index(client, message):
    try:
        collection.update_one(
            {"message_id": message.id},
            {"$set": {"message_id": message.id}},
            upsert=True
        )
        logger.info(f"✅ Auto-Indexed video: {message.id}")

    except Exception as e:
        logger.error(f"❌ Auto-Indexing Error: {e}")

# 🔹 ✅ Fix /files Command (Counts Indexed Videos)
@bot.on_message(filters.command("files") & filters.user(OWNER_ID))
async def get_file_count(client, message):
    try:
        count = collection.count_documents({})
        await message.reply_text(f"📂 Total indexed videos: {count}")
    except Exception as e:
        logger.error(f"❌ File Count Error: {e}")
        await message.reply_text("❌ Error fetching file count.")

# 🔹 ✅ Fix Repeating Video Issue (Now Truly Random)
@bot.on_message(filters.command("random"))
async def send_random_video(client, message):
    try:
        video_docs = list(collection.find({}))
        if not video_docs:
            await message.reply_text("⚠ No videos available. Add videos to the channel first!")
            return

        selected_videos = random.sample(video_docs, min(5, len(video_docs)))  # Pick random 5 videos

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

# 🔹 ✅ Start Bot
if __name__ == "__main__":
    bot.run()
