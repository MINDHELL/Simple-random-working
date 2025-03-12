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

# 🔰 Environment Variables (Ensure OWNER_ID is an integer)
API_ID = "27788368"
API_HASH = "9df7e9ef3d7e4145270045e5e43e1081"
BOT_TOKEN = "7725707727:AAFtx6Sy-q6GgB9eaPoN2-oYPx2D6hjnc1g"
MONGO_URL = "mongodb+srv://aarshhub:6L1PAPikOnAIHIRA@cluster0.6shiu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
CHANNEL_ID = "-1002492623985"
OWNER_ID = int("6860316927")  # 🔥 Ensure it's an integer

# 🔰 Initialize Bot & Database
bot = Client("video_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
mongo = MongoClient(MONGO_URL)
db = mongo["VideoBot"]
collection = db["videos"]

# 🔍 Log All Messages for Debugging
@bot.on_message(filters.text)
async def log_messages(client, message):
    logger.info(f"📩 Received: {message.text} from {message.from_user.id}")

# 🔰 Index Videos (Fixing Command Detection)
@bot.on_message(filters.command("index") & filters.user(OWNER_ID))
async def index_videos(client, message):
    logger.info(f"✅ Received /index command from {message.from_user.id}")
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

# 🔰 Run the Bot
if __name__ == "__main__":
    threading.Thread(target=start_health_check, daemon=True).start()
    logger.info("🚀 Bot is starting...")
    bot.run()
