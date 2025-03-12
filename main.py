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

# 🔰 Environment Variables (Filled)
API_ID = "27788368"
API_HASH = "9df7e9ef3d7e4145270045e5e43e1081"
BOT_TOKEN = "7725707727:AAFtx6Sy-q6GgB9eaPoN2-oYPx2D6hjnc1g"
MONGO_URL = "mongodb+srv://aarshhub:6L1PAPikOnAIHIRA@cluster0.6shiu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
CHANNEL_ID = "-1002492623985"
OWNER_ID = "6860316927"

# 🔰 Initialize Bot & Database
bot = Client("video_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
mongo = MongoClient(MONGO_URL)
db = mongo["VideoBot"]
collection = db["videos"]

# 🔰 Fetch & Send a Random Video Without Forward Tag
async def send_random_video(client, chat_id):
    video_docs = list(collection.find())
    if not video_docs:
        await client.send_message(chat_id, "⚠ No videos available. Use /index first!")
        return
    random_video = random.choice(video_docs)
    
    try:
        await client.copy_message(chat_id=chat_id, from_chat_id=CHANNEL_ID, message_id=random_video["message_id"])
    except Exception as e:
        await client.send_message(chat_id, "❌ Error: Failed to send video.")
        logger.error(f"Error sending video: {e}")

# 🔰 Index Videos (Fixed)
@bot.on_message(filters.command("index") & filters.user(OWNER_ID))
async def index_videos(client, message):
    await message.reply_text("🔄 Indexing videos... This may take some time.")

    indexed_count = 0
    max_id = await client.get_messages(CHANNEL_ID, 1)  # ✅ Get latest message ID
    if not max_id:
        await message.reply_text("⚠ Failed to fetch channel messages. Check bot permissions!")
        return

    message_ids = list(range(1, max_id.id + 1))  # ✅ Generate IDs from 1 to latest
    chunk_size = 100  # ✅ Fetch 100 messages per batch

    try:
        for i in range(0, len(message_ids), chunk_size):
            messages = await client.get_messages(CHANNEL_ID, message_ids[i:i+chunk_size])
            for msg in messages:
                if msg and msg.video:
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
        await message.reply_text("❌ Error: Failed to fetch the channel details.")
        logger.error(f"Error in /index command: {e}")

# 🔰 Start Command with Inline Button
@bot.on_message(filters.command("start"))
async def start(client, message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎥 Get Random Video", callback_data="get_random_video")]
    ])
    await message.reply_text("Welcome! Click the button below to get a random video:", reply_markup=keyboard)

# 🔰 Callback for Random Video
@bot.on_callback_query(filters.regex("get_random_video"))
async def random_video_callback(client, callback_query: CallbackQuery):
    await send_random_video(client, callback_query.message.chat.id)
    await callback_query.answer()

# 🔰 Run the Bot
if __name__ == "__main__":
    threading.Thread(target=start_health_check, daemon=True).start()
    bot.run()
