import os
import logging
import random
import threading
from pyrogram import Client, filters
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
CHANNEL_ID = "-1002492623985"  # Channel where videos are indexed
OWNER_ID = "6860316927"  # Your Telegram ID

# 🔰 Initialize Bot & Database
bot = Client("video_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
mongo = MongoClient(MONGO_URL)
db = mongo["VideoBot"]
collection = db["videos"]

# 🔹 Function to Fetch & Send a Random Video
async def send_random_video(client, chat_id):
    video_docs = list(collection.find())
    if not video_docs:
        await client.send_message(chat_id, "⚠ No videos available. Use /index first!")
        return

    random_video = random.choice(video_docs)

    try:
        video_msg = await client.get_messages(CHANNEL_ID, random_video["message_id"])
        if video_msg and video_msg.video:
            await client.send_video(
                chat_id=chat_id,
                video=video_msg.video.file_id,
                caption="🎥 Here’s your random video!"
            )
        else:
            await client.send_message(chat_id, "⚠ Error: Video not found!")
    except Exception as e:
        logger.error(f"❌ Error sending video: {e}")
        await client.send_message(chat_id, "❌ Error: Failed to send video.")

# 🔹 Command to Index Videos (Owner Only) – Fixed for Bots
@bot.on_message(filters.command("index") & filters.user(OWNER_ID))
async def index_videos(client, message):
    await message.reply_text("🔄 Indexing videos... This may take some time.")

    indexed_count = 0
    try:
        async for msg in client.search_messages(CHANNEL_ID, filter="video"):
            collection.update_one(
                {"message_id": msg.id},  
                {"$set": {"message_id": msg.id}}, 
                upsert=True
            )
            indexed_count += 1

        if indexed_count > 0:
            await message.reply_text(f"✅ Indexing completed! {indexed_count} videos added.")
            await client.send_message(OWNER_ID, f"📢 Successfully indexed {indexed_count} videos!")
        else:
            await message.reply_text("⚠ No videos found in the channel. Make sure the bot has access!")

    except Exception as e:
        logger.error(f"❌ Indexing Error: {e}")
        await message.reply_text("❌ Error during indexing. Check logs.")

# 🔹 Start Command with Inline Button
@bot.on_message(filters.command("start"))
async def start(client, message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎥 Get Random Video", callback_data="get_random_video")]
    ])
    await message.reply_text("Welcome! Click the button below to get a random video:", reply_markup=keyboard)

# 🔹 Callback for Random Video
@bot.on_callback_query(filters.regex("get_random_video"))
async def random_video_callback(client, callback_query: CallbackQuery):
    await send_random_video(client, callback_query.message.chat.id)
    await callback_query.answer()

# 🔹 Run the Bot (With Health Check)
if __name__ == "__main__":
    threading.Thread(target=start_health_check, daemon=True).start()
    bot.run()
