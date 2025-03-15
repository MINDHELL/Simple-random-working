import os
import logging
import random
import threading
from pyrogram import Client, filters
from pyrogram.errors import PeerIdInvalid
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pymongo import MongoClient
from health_check import start_health_check

# 🔰 Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔰 Environment Variables
API_ID = "27788368"
API_HASH = "9df7e9ef3d7e4145270045e5e43e1081"
BOT_TOKEN = "7725707727:AAFtx6Sy-q6GgB9eaPoN2-oYPx2D6hjnc1g"
MONGO_URL = "mongodb+srv://aarshhub:6L1PAPikOnAIHIRA@cluster0.6shiu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
CHANNEL_ID = "-1002492623985"  # Ensure it's an integer (negative for channels)
OWNER_ID = "6860316927"  # Ensure it's an integer

# 🔰 Initialize Bot & Database
bot = Client("video_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
mongo = MongoClient(MONGO_URL)
db = mongo["VideoBot"]
collection = db["videos"]

# ✅ Command to Check MongoDB Connection
@bot.on_message(filters.command("checkdb") & filters.user(OWNER_ID))
async def check_database(client, message):
    try:
        mongo.admin.command('ping')  # Checks if MongoDB is reachable
        await message.reply_text("✅ **Database Connection:** Active!")
    except Exception as e:
        logger.error(f"❌ Database Error: {e}")
        await message.reply_text("❌ **Database Connection Failed!** Check MongoDB URL.")

# ✅ Improved Random Video Fetching
async def send_random_video(client, chat_id):
    try:
        video_docs = list(collection.find())
        if not video_docs:
            await client.send_message(chat_id, "⚠ No videos available. Use /index first!")
            return

        used_videos = set()

        for _ in range(5):  # Try up to 5 times to get a valid video
            random_video = random.choice(video_docs)
            if random_video["message_id"] in used_videos:
                continue  

            used_videos.add(random_video["message_id"])
            logger.info(f"🔍 Fetching video with message_id: {random_video['message_id']}")

            try:
                video_msg = await client.get_messages(CHANNEL_ID, message_ids=[random_video["message_id"]])
                if video_msg and video_msg.video:
                    await client.send_video(
                        chat_id=chat_id,
                        video=video_msg.video.file_id,
                        caption="🎥 Here’s your random video!"
                    )
                    return
            except Exception as e:
                logger.error(f"⚠ Error fetching video: {e}")

        await client.send_message(chat_id, "⚠ Error: Could not fetch any valid video.")

    except PeerIdInvalid:
        logger.error("❌ Bot does not have access to the channel!")
        await client.send_message(chat_id, "❌ Error: Ensure the bot is an admin in the channel.")

    except Exception as e:
        logger.error(f"❌ Error sending video: {e}")
        await client.send_message(chat_id, "❌ Error: Failed to send video.")

# ✅ Improved /index Command (Prevents Duplicates)
@bot.on_message(filters.command("index") & filters.user(OWNER_ID))
async def index_videos(client, message):
    await message.reply_text("🔄 Indexing videos... Please wait.")

    indexed_count = 0
    try:
        existing_videos = {doc["message_id"] for doc in collection.find()}

        async for msg in client.get_chat_history(CHANNEL_ID, limit=2000):
            if msg.video and msg.id not in existing_videos:
                collection.insert_one({"message_id": msg.id, "file_id": msg.video.file_id})
                indexed_count += 1

        if indexed_count > 0:
            await message.reply_text(f"✅ **Indexing Complete:** {indexed_count} new videos added.")
            await client.send_message(OWNER_ID, f"📢 Indexed {indexed_count} new videos!")
        else:
            await message.reply_text("⚠ No new videos found. Everything is already indexed.")

    except PeerIdInvalid:
        logger.error("❌ Bot does not have access to the channel!")
        await message.reply_text("❌ **Error:** Ensure the bot is an admin in the channel.")

# ✅ Improved /files Command (Accurate Count)
@bot.on_message(filters.command("files") & filters.user(OWNER_ID))
async def get_file_count(client, message):
    count = collection.count_documents({})
    await message.reply_text(f"📂 **Total Indexed Videos:** `{count}`")

# ✅ Start Command with Inline Button
@bot.on_message(filters.command("start"))
async def start(client, message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎥 Get Random Video", callback_data="get_random_video")]
    ])
    await message.reply_text("👋 Welcome! Click below to get a random video:", reply_markup=keyboard)

# ✅ Callback for Random Video
@bot.on_callback_query(filters.regex("get_random_video"))
async def random_video_callback(client, callback_query: CallbackQuery):
    await send_random_video(client, callback_query.message.chat.id)
    await callback_query.answer()

# ✅ Run the Bot (With Health Check)
if __name__ == "__main__":
    threading.Thread(target=start_health_check, daemon=True).start()
    bot.run()
