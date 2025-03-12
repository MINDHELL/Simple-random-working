import os
import logging
import random
import threading
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton
from pymongo import MongoClient
from health_check import start_health_check

# 🔰 Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔰 Environment Variables
API_ID = int(os.getenv("API_ID", "27788368"))
API_HASH = os.getenv("API_HASH", "9df7e9ef3d7e4145270045e5e43e1081")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7725707727:AAFtx6Sy-q6GgB9eaPoN2-oYPx2D6hjnc1g")
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://aarshhub:6L1PAPikOnAIHIRA@cluster0.6shiu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "-1002492623985"))
OWNER_ID = int(os.getenv("OWNER_ID", "6860316927"))

# 🔰 Initialize Bot & Database
bot = Client("video_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
mongo = MongoClient(MONGO_URL)
db = mongo["VideoBot"]
collection = db["videos"]

# 🔰 Function to Fetch & Send a Random Video
async def send_random_video(client, chat_id):
    video_docs = list(collection.find())
    if not video_docs:
        await client.send_message(chat_id, "⚠ No videos available. Use /index first!")
        return
    
    random_video = random.choice(video_docs)
    file_id = random_video.get("file_id")
    if file_id:
        await client.send_video(chat_id, video=file_id, caption="🎥 Here's your random video!")
    else:
        await client.send_message(chat_id, "⚠ Error: This video is missing a file_id.")

# 🔰 Fixed `/index` Command (Now Works for All Channels)
@bot.on_message(filters.command("index") & filters.user(OWNER_ID))
async def index_videos(client, message):
    try:
        await message.reply_text("🔄 Indexing videos... Please wait.")
        indexed_count = 0

        async for msg in client.iter_messages(CHANNEL_ID, limit=1000):
            if msg.video:
                collection.update_one(
                    {"message_id": msg.id},
                    {"$set": {
                        "message_id": msg.id,
                        "file_id": msg.video.file_id
                    }},
                    upsert=True
                )
                indexed_count += 1

        await message.reply_text(f"✅ Indexing completed! {indexed_count} videos added.")

    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

# 🔰 Start Command with Reply Keyboard
@bot.on_message(filters.command("start"))
async def start(client, message):
    keyboard = ReplyKeyboardMarkup(
        [[KeyboardButton("🎥 Get Random Video")]],
        resize_keyboard=True
    )
    await message.reply_text("Welcome! Click the button below to get a random video:", reply_markup=keyboard)

# 🔰 Handle Reply Keyboard Button Press
@bot.on_message(filters.text & filters.regex("🎥 Get Random Video"))
async def random_video_command(client, message):
    await send_random_video(client, message.chat.id)

# 🔰 Run the Bot
if __name__ == "__main__":
    threading.Thread(target=start_health_check, daemon=True).start()
    bot.run()
