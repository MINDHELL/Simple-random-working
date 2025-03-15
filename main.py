import os
import random
import logging
from pyrogram import Client, filters
from pymongo import MongoClient
from pyrogram.enums import MessagesFilter
from flask import Flask
import threading

# ✅ Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Load Environment Variables
API_ID = "27788368"
API_HASH = "9df7e9ef3d7e4145270045e5e43e1081"
BOT_TOKEN = "7725707727:AAFtx6Sy-q6GgB9eaPoN2-oYPx2D6hjnc1g"
MONGO_URL = "mongodb+srv://aarshhub:6L1PAPikOnAIHIRA@cluster0.6shiu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
CHANNEL_ID = "-1002492623985"  # Ensure it's negative
OWNER_ID = "6860316927"  # Your Telegram ID

# ✅ MongoDB Connection
mongo_client = MongoClient(MONGO_URL)
db = mongo_client["telegram_bot"]
collection = db["videos"]

# ✅ Pyrogram Client (Bot)
bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ✅ Flask App for Health Check
app = Flask(__name__)

@app.route("/")
def health_check():
    return "Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

# ✅ Background Thread for Flask
threading.Thread(target=run_flask, daemon=True).start()

# 🔄 **Index Videos** Command
@bot.on_message(filters.command("index") & filters.user(OWNER_ID))
async def index_videos(client, message):
    await message.reply_text("🔄 Indexing videos... Please wait.")

    indexed_count = 0
    try:
        async for msg in client.search_messages(CHANNEL_ID, filter=MessagesFilter.VIDEO, limit=1000):
            if msg.video:
                collection.update_one(
                    {"message_id": msg.id},  
                    {"$set": {"message_id": msg.id}}, 
                    upsert=True
                )
                indexed_count += 1

        await message.reply_text(f"✅ Indexed {indexed_count} videos!")
    except Exception as e:
        logger.error(f"❌ Error indexing videos: {e}")
        await message.reply_text("❌ Error: Failed to index videos.")

# 📂 **Show Total Indexed Files** Command
@bot.on_message(filters.command("files") & filters.user(OWNER_ID))
async def show_file_count(client, message):
    file_count = collection.count_documents({})
    await message.reply_text(f"📂 Total indexed videos: {file_count}")

# 🎥 **Send Random Video** Command
@bot.on_message(filters.command("random"))
async def send_random_video(client, message):
    videos = list(collection.find())
    
    if not videos:
        await message.reply_text("⚠ No videos found. Use /index first!")
        return

    random_video = random.choice(videos)
    message_id = random_video["message_id"]

    try:
        await client.copy_message(
            chat_id=message.chat.id,
            from_chat_id=CHANNEL_ID,
            message_id=message_id
        )
    except Exception as e:
        logger.error(f"❌ Error sending video: {e}")
        await message.reply_text("❌ Error: Could not fetch video.")

# ✅ Start Bot
bot.start()
print("Bot is running...")

bot.run()
