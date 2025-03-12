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

# 🔰 Function to fetch & send a random video
async def send_random_video(client, chat_id):
    video_docs = list(collection.find())
    
    if not video_docs:
        await client.send_message(chat_id, "⚠ No videos available. Use /index first!")
        return

    random_video = random.choice(video_docs)
    
    await client.send_video(
        chat_id=chat_id, 
        video=random_video["file_id"],  # ✅ Send video without forward tag
        caption=random_video["title"] if "title" in random_video else "🎥 Random Video"
    )

# 🔰 Command to index videos (Owner Only)
@bot.on_message(filters.command("index") & filters.user(OWNER_ID))
async def index_videos(client, message):
    await message.reply_text("🔄 Indexing videos... This may take some time.")

    indexed_count = 0

    # ✅ Use iter_history() to safely fetch up to 1000 messages
    async for msg in client.iter_history(CHANNEL_ID, limit=1000):
        if msg.video:
            # ✅ Store message_id & caption/title
            collection.update_one(
                {"file_id": msg.video.file_id},  
                {"$set": {
                    "file_id": msg.video.file_id,  
                    "message_id": msg.id,  
                    "title": msg.caption or "Untitled Video"
                }}, 
                upsert=True
            )
            indexed_count += 1

    if indexed_count > 0:
        await message.reply_text(f"✅ Indexing completed! {indexed_count} videos added.")
        await client.send_message(OWNER_ID, f"📢 Successfully indexed {indexed_count} videos!")
    else:
        await message.reply_text("⚠ No videos found in the channel. Make sure the bot has access!")

# 🔰 Start Command with Reply Keyboard Button
@bot.on_message(filters.command("start"))
async def start(client, message):
    keyboard = ReplyKeyboardMarkup(
        [[KeyboardButton("🎥 Get Random Video")]], resize_keyboard=True
    )
    await message.reply_text("Welcome! Use the button below to get a random video:", reply_markup=keyboard)

# 🔰 Listen for Button Click via Text Message
@bot.on_message(filters.text & filters.regex("🎥 Get Random Video"))
async def random_video_command(client, message):
    await send_random_video(client, message.chat.id)

# 🔰 Run the Bot
if __name__ == "__main__":
    threading.Thread(target=start_health_check, daemon=True).start()
    bot.run()
