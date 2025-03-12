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

# ✅ Initialize Bot
bot = Client("random_video_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ✅ Setup MongoDB
client = pymongo.MongoClient(MONGO_URL)
db = client["TelegramBot"]
collection = db["Videos"]

# ✅ Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Keyboard
main_keyboard = ReplyKeyboardMarkup(
    [["🎥 Get Random Video"], ["📁 Index Videos"]],
    resize_keyboard=True
)


# ✅ /start Command
@bot.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text(
        "👋 Welcome! Use the buttons below to get a random video or index videos.",
        reply_markup=main_keyboard
    )


# ✅ /index Command (Fixed)
@bot.on_message(filters.command("index") & filters.user(OWNER_ID))
async def index_videos(client, message):
    try:
        await message.reply_text("🔄 Indexing videos... Please wait.")

        # Fetch the latest message in the channel
        last_message = await client.get_messages(CHANNEL_ID, limit=1)
        if not last_message:
            await message.reply_text("❌ No messages found in the channel.")
            return
        
        last_msg_id = last_message[0].id
        indexed_count = 0

        for msg_id in range(last_msg_id, 0, -1):
            msg = await client.get_messages(CHANNEL_ID, msg_id)
            if msg and msg.video:
                collection.update_one(
                    {"message_id": msg.id},
                    {"$set": {"message_id": msg.id, "file_id": msg.video.file_id}},
                    upsert=True
                )
                indexed_count += 1

        await message.reply_text(f"✅ Indexing completed! {indexed_count} videos added.")

    except Exception as e:
        logger.error(f"Error in indexing: {str(e)}")
        await message.reply_text(f"❌ Error: {str(e)}")


# ✅ Get Random Video (Reply Keyboard)
@bot.on_message(filters.text & filters.regex("🎥 Get Random Video"))
async def send_random_video(client, message):
    try:
        total_videos = collection.count_documents({})
        if total_videos == 0:
            await message.reply_text("❌ No videos found in the database.")
            return

        random_video = collection.find().limit(1).skip(random.randint(0, total_videos - 1)).next()
        await client.send_video(
            chat_id=message.chat.id,
            video=random_video["file_id"],
            caption="Here's your random video! 🎥"
        )

    except Exception as e:
        logger.error(f"Error sending random video: {str(e)}")
        await message.reply_text("❌ An error occurred while fetching a video.")


# ✅ Start Bot
if __name__ == "__main__":
    bot.run()
