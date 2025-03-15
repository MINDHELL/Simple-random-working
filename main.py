import os
import logging
import random
import threading
from pyrogram import Client, filters
from pyrogram.errors import PeerIdInvalid, FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pymongo import MongoClient
from health_check import start_health_check
import time

# 🔰 Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔰 Environment Variables
API_ID = "27788368"
API_HASH = "9df7e9ef3d7e4145270045e5e43e1081"
BOT_TOKEN = "7725707727:AAFtx6Sy-q6GgB9eaPoN2-oYPx2D6hjnc1g"
MONGO_URL = "mongodb+srv://aarshhub:6L1PAPikOnAIHIRA@cluster0.6shiu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
CHANNEL_ID = "-1002492623985"  # Ensure it's negative for channels
OWNER_ID = "6860316927"  # Your Telegram ID

# 🔰 Initialize Bot & Database
bot = Client("video_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
mongo = MongoClient(MONGO_URL)
db = mongo["VideoBot"]
collection = db["videos"]

# 🔹 Function to Fetch & Send a Truly Random Video
async def send_random_video(client, chat_id):
    try:
        video_docs = list(collection.find({}))  # Get all indexed videos
        if not video_docs:
            await client.send_message(chat_id, "⚠ No videos available. Use /index first!")
            return

        random.shuffle(video_docs)  # Shuffle to ensure true randomness
        sent_videos = set()

        for _ in range(min(10, len(video_docs))):  # Try different videos
            random_video = random.choice(video_docs)
            message_id = random_video["message_id"]

            if message_id in sent_videos:
                continue  # Skip already sent videos

            logger.info(f"🔍 Fetching video with message_id: {message_id}")

            try:
                await client.copy_message(
                    chat_id=chat_id,
                    from_chat_id=CHANNEL_ID,
                    message_id=message_id
                )
                sent_videos.add(message_id)
                return  # Stop after successfully sending one video
            except FloodWait as e:
                logger.warning(f"⏳ FloodWait: Sleeping for {e.value} seconds...")
                time.sleep(e.value)
            except Exception as e:
                logger.error(f"⚠ Error fetching video: {e}")

        await client.send_message(chat_id, "⚠ Error: Could not fetch a video.")

    except PeerIdInvalid:
        logger.error("❌ Peer ID Invalid: Ensure the bot is an admin in the channel!")
        await client.send_message(chat_id, "❌ Error: Bot does not have access to the channel!")

    except Exception as e:
        logger.error(f"❌ Error sending video: {e}")
        await client.send_message(chat_id, "❌ Error: Failed to send video.")

# 🔹 Command to Index Videos (Owner Only)
@bot.on_message(filters.command("index") & filters.user(OWNER_ID))
async def index_videos(client, message):
    await message.reply_text("🔄 Indexing videos... This may take a while.")
    
    indexed_count = 0
    try:
        async for msg in client.get_chat_history(CHANNEL_ID, limit=2000):
            if msg.video:
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
            await message.reply_text("⚠ No videos found in the channel!")

    except PeerIdInvalid:
        logger.error("❌ Bot does not have access to the channel. Make sure the bot is an admin!")
        await message.reply_text("❌ Error: Bot does not have access to the channel!")

    except Exception as e:
        logger.error(f"❌ Error during indexing: {e}")
        await message.reply_text("❌ Error: Failed to index videos.")

# 🔹 Command to Get Total Indexed Files
@bot.on_message(filters.command("files") & filters.user(OWNER_ID))
async def get_file_count(client, message):
    try:
        count = collection.count_documents({})
        await message.reply_text(f"📂 Total indexed videos: {count}")
    except Exception as e:
        logger.error(f"❌ Error fetching file count: {e}")
        await message.reply_text("❌ Error: Could not retrieve file count.")

# 🔹 Start Command with Inline Button
@bot.on_message(filters.command("start"))
async def start(client, message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎥 Get Random Video", callback_data="get_random_video")],
        [InlineKeyboardButton("🔄 Re-index Videos", callback_data="reindex_videos")]
    ])
    await message.reply_text("Welcome! Click a button below:", reply_markup=keyboard)

# 🔹 Callback for Random Video
@bot.on_callback_query(filters.regex("get_random_video"))
async def random_video_callback(client, callback_query: CallbackQuery):
    await send_random_video(client, callback_query.message.chat.id)
    await callback_query.answer()

# 🔹 Callback for Re-indexing Videos (Owner Only)
@bot.on_callback_query(filters.regex("reindex_videos") & filters.user(OWNER_ID))
async def reindex_videos_callback(client, callback_query: CallbackQuery):
    await index_videos(client, callback_query.message)
    await callback_query.answer()

# 🔹 Run the Bot (With Health Check)
if __name__ == "__main__":
    threading.Thread(target=start_health_check, daemon=True).start()
    bot.run()
