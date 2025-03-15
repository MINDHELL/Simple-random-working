import os
import logging
import random
import threading
import traceback
from flask import Flask
from pyrogram import Client, filters
from pyrogram.errors import PeerIdInvalid, ChatAdminRequired
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pymongo import MongoClient

# 🔰 Logging Setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# 🔰 Environment Variables
API_ID = "27788368"
API_HASH = "9df7e9ef3d7e4145270045e5e43e1081"
BOT_TOKEN = "7725707727:AAFtx6Sy-q6GgB9eaPoN2-oYPx2D6hjnc1g"
MONGO_URL = "mongodb+srv://aarshhub:6L1PAPikOnAIHIRA@cluster0.6shiu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
CHANNEL_ID = "-1002492623985"  # Ensure it's negative
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

# 🔹 Improved Indexing Function
@bot.on_message(filters.command("index") & filters.user(OWNER_ID))
async def index_videos(client, message):
    try:
        await message.reply_text("🔄 Indexing videos... Please wait.")

        total, duplicate = 0, 0
        async for msg in client.get_chat_history(CHANNEL_ID, limit=10000):
            if msg.video:
                saved = await save_file(msg)
                if saved:
                    total += 1
                else:
                    duplicate += 1

        await message.reply_text(f"✅ Indexing completed!\n🆕 New videos: {total}\n⚠ Duplicates: {duplicate}")
        logger.info(f"✅ Indexing completed! New: {total}, Duplicates: {duplicate}")

    except ChatAdminRequired:
        error_msg = "❌ Error: Bot must be an admin in the channel!"
        logger.error(error_msg)
        await message.reply_text(error_msg)

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

# 🔹 Function to Fetch & Send a Random Video
async def send_random_video(client, chat_id):
    try:
        video_docs = list(collection.find())
        if not video_docs:
            await client.send_message(chat_id, "⚠ No videos available. Use /index first!")
            return

        random.shuffle(video_docs)
        selected_video = random.choice(video_docs)

        logger.info(f"🔍 Fetching video with message_id: {selected_video['message_id']}")
        try:
            await client.copy_message(chat_id, CHANNEL_ID, selected_video["message_id"])
            return
        except Exception as e:
            logger.error(f"⚠ Error copying video: {e}")

        await client.send_message(chat_id, "⚠ Error: Could not fetch any video.")
    
    except PeerIdInvalid:
        logger.error("❌ Peer ID Invalid: Ensure the bot is an admin in the channel!")
        await client.send_message(chat_id, "❌ Error: Bot does not have access to the channel.")

    except Exception as e:
        logger.error(f"❌ Error sending video: {e}")
        logger.error(traceback.format_exc())
        await client.send_message(chat_id, "❌ Error: Failed to send video.")

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
