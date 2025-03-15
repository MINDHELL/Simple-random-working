import os
import logging
import random
import threading
from pyrogram import Client, filters
from pyrogram.errors import PeerIdInvalid
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
CHANNEL_ID = -1002492623985  # Ensure it's an integer (negative for channels)
OWNER_ID = 6860316927  # Ensure it's an integer

# 🔰 Initialize Bot & Database
bot = Client("video_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
mongo = MongoClient(MONGO_URL)
db = mongo["VideoBot"]
collection = db["videos"]

# 🔹 Function to Fetch & Send a Random Video
async def send_random_video(client, chat_id):
    try:
        video_docs = list(collection.find())
        if not video_docs:
            await client.send_message(chat_id, "⚠ No videos available. Use /index first!")
            return

        random_video = random.choice(video_docs)
        message_id = random_video.get("message_id")
        logger.info(f"🔍 Fetching video with message_id: {message_id}")

        # ✅ Ensure bot has access before fetching
        try:
            chat_info = await client.get_chat(CHANNEL_ID)
            logger.info(f"✅ Bot has access to the channel: {chat_info.title}")
        except PeerIdInvalid:
            logger.error("❌ Bot does not have access to the channel. Make sure the bot is an admin!")
            await client.send_message(chat_id, "❌ Error: Bot does not have access to the channel. Make sure the bot is an admin!")
            return

        # ✅ Fetch video message correctly
        video_msgs = await client.get_messages(CHANNEL_ID, message_ids=[message_id])

        if not video_msgs or not isinstance(video_msgs, list) or not video_msgs[0]:
            await client.send_message(chat_id, "⚠ Error: Could not fetch video.")
            return

        video_msg = video_msgs[0]  # ✅ Extract first message from the list

        if video_msg.video:
            await client.send_video(
                chat_id=chat_id,
                video=video_msg.video.file_id,
                caption="🎥 Here’s your random video!"
            )
        else:
            await client.send_message(chat_id, "⚠ Error: Video not found in the selected message.")

    except Exception as e:
        logger.error(f"❌ Error sending video: {e}")
        await client.send_message(chat_id, "❌ Error: Failed to send video.")

# 🔹 Command to Index Videos (Owner Only)
@bot.on_message(filters.command("index") & filters.user(OWNER_ID))
async def index_videos(client, message):
    await message.reply_text("🔄 Indexing videos... This may take some time.")
    
    indexed_count = 0
    try:
        async for msg in client.get_chat_history(CHANNEL_ID, limit=1000):  # ✅ Corrected method
            if msg.video:
                if not collection.find_one({"message_id": msg.id}):  # ✅ Prevent duplicates
                    collection.insert_one({"message_id": msg.id})
                    indexed_count += 1

        if indexed_count > 0:
            await message.reply_text(f"✅ Indexing completed! {indexed_count} videos added.")
            await client.send_message(OWNER_ID, f"📢 Successfully indexed {indexed_count} videos!")
        else:
            await message.reply_text("⚠ No new videos found in the channel.")

    except PeerIdInvalid:
        logger.error("❌ Bot does not have access to the channel. Make sure the bot is an admin!")
        await message.reply_text("❌ Error: Bot does not have access to the channel. Make sure the bot is an admin!")

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
