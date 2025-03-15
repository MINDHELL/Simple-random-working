import os
import logging
import traceback
import threading
from flask import Flask
from pyrogram import Client, filters
from pymongo import MongoClient

# 🔰 Logging Setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# 🔰 Environment Variables
API_ID = "27788368"
API_HASH = "9df7e9ef3d7e4145270045e5e43e1081"
BOT_TOKEN = "7725707727:AAFtx6Sy-q6GgB9eaPoN2-oYPx2D6hjnc1g"
MONGO_URL = "mongodb+srv://aarshhub:6L1PAPikOnAIHIRA@cluster0.6shiu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
MIRROR_CHANNEL_ID = "-1002659652578"  # Your Private Mirror Channel ID
OWNER_ID = int("6860316927")  # Your Telegram ID

# 🔰 Initialize Bot & Database
bot = Client("video_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
mongo = MongoClient(MONGO_URL)
db = mongo["VideoBot"]
collection = db["videos"]

# 🔹 Function to Save File to DB
async def save_file(msg):
    if not collection.find_one({"message_id": msg.id}):
        collection.insert_one({"message_id": msg.id, "file_id": msg.video.file_id})
        return True
    return False

# 🔹 Fixed Indexing Function (Using Mirror Channel)
@bot.on_message(filters.command("index") & filters.user(OWNER_ID))
async def index_videos(client, message):
    try:
        await message.reply_text("🔄 Indexing videos... Please wait.")
        total, duplicate = 0, 0

        async for msg in bot.get_chat_history(MIRROR_CHANNEL_ID, limit=10000):
            if msg.video:
                saved = await save_file(msg)
                if saved:
                    total += 1
                else:
                    duplicate += 1

        await message.reply_text(f"✅ Indexing completed!\n🆕 New videos: {total}\n⚠ Duplicates: {duplicate}")
        logger.info(f"✅ Indexing completed! New: {total}, Duplicates: {duplicate}")

    except Exception as e:
        error_msg = f"❌ Error in /index: {e}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        await message.reply_text(error_msg)

# 🔹 Command to Get Total Indexed Files
@bot.on_message(filters.command("files") & filters.user(OWNER_ID))
async def get_file_count(client, message):
    try:
        count = collection.count_documents({})
        await message.reply_text(f"📂 Total indexed videos: {count}")
        logger.info(f"📂 Total indexed videos: {count}")

    except Exception as e:
        error_msg = f"❌ Error in /files: {e}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        await message.reply_text(error_msg)

# 🔹 Dummy Flask Server to Fix Koyeb Health Check
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

# 🔹 Run the Bot with Flask Server
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()  # Start Flask in a separate thread
    bot.run()
