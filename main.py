import os
import logging
import random
import threading
from flask import Flask
from pyrogram import Client, filters
from pymongo import MongoClient

# 🔰 Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔰 Environment Variables (Filled)
API_ID = "27788368"
API_HASH = "9df7e9ef3d7e4145270045e5e43e1081"
BOT_TOKEN = "7725707727:AAFtx6Sy-q6GgB9eaPoN2-oYPx2D6hjnc1g"
MONGO_URL = "mongodb+srv://aarshhub:6L1PAPikOnAIHIRA@cluster0.6shiu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
CHANNEL_ID = "-1002492623985"  # Ensure it's negative
OWNER_ID = "6860316927"  # Your Telegram ID

# 🔰 Initialize Bot & Database
bot = Client("video_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
mongo = MongoClient(MONGO_URL)
db = mongo["VideoBot"]
collection = db["videos"]

# ✅ Debug Test Command
@bot.on_message(filters.command("test"))
async def test_command(client, message):
    print("✅ Bot received /test command")
    await message.reply_text("✅ Bot is running and responding!")

# ✅ Debugging: Check User ID
@bot.on_message(filters.command("whoami"))
async def whoami(client, message):
    print(f"🆔 Your user ID: {message.from_user.id}")
    await message.reply_text(f"🆔 Your user ID: `{message.from_user.id}`")

# 🔹 Command to Index Videos (Owner Only)
@bot.on_message(filters.command("index"))
async def index_videos(client, message):
    print(f"📌 Received /index command from {message.from_user.id}")  # DEBUG PRINT

    # ❌ Fix Owner Check: Only allow OWNER_ID
    if message.from_user.id != OWNER_ID:
        await message.reply_text("❌ You are not authorized to use this command.")
        return

    await message.reply_text("🔄 Indexing videos... Please wait.")
    
    total, duplicate = 0, 0
    async for msg in client.iter_messages(CHANNEL_ID, filter="video"):
        if msg.video:
            if not collection.find_one({"message_id": msg.id}):
                collection.insert_one({"message_id": msg.id, "file_id": msg.video.file_id})
                total += 1
            else:
                duplicate += 1

    print(f"✅ Indexing completed! New: {total}, Duplicates: {duplicate}")  # DEBUG PRINT
    await message.reply_text(f"✅ Indexing completed!\n🆕 New videos: {total}\n⚠ Duplicates: {duplicate}")

# 🔹 Command to Get Total Indexed Files
@bot.on_message(filters.command("files"))
async def get_file_count(client, message):
    print(f"📌 Received /files command from {message.from_user.id}")  # DEBUG PRINT

    # ❌ Fix Owner Check: Only allow OWNER_ID
    if message.from_user.id != OWNER_ID:
        await message.reply_text("❌ You are not authorized to use this command.")
        return

    count = collection.count_documents({})
    print(f"📂 Total indexed videos: {count}")  # DEBUG PRINT
    await message.reply_text(f"📂 Total indexed videos: {count}")

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
    print("🚀 Bot is starting...")  # DEBUG PRINT
    bot.run()
