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

# 🔰 Function to fetch & send a random video (Removes Forward Tag)
async def send_random_video(client, chat_id):
    video_docs = list(collection.find())
    if not video_docs:
        await client.send_message(chat_id, "⚠ No videos available. Use /index first!")
        return
    
    random_video = random.choice(video_docs)
    try:
        message = await client.get_messages(CHANNEL_ID, random_video["message_id"])
        if message and message.video:
            await client.send_video(
                chat_id=chat_id,
                video=message.video.file_id,  # ✅ Removes forward tag
                caption="Thanks 😊"
            )
        else:
            await client.send_message(chat_id, "⚠ The selected message is not a video.")
    except Exception as e:
        logger.error(f"Error sending video: {e}")
        await client.send_message(chat_id, "⚠ Error fetching video. Try again later.")

# 🔰 Command to index videos (Owner Only)
@bot.on_message(filters.command("index") & filters.user(OWNER_ID))
async def index_videos(client, message):
    await message.reply_text("🔄 Indexing videos... This may take some time.")
    
    indexed_count = 0
    last_message_id = 2000  # ✅ Adjust this if needed (set it to the latest message ID)
    batch_size = 200  # ✅ Fetch messages in batches of 200

    while last_message_id > 0:
        try:
            message_ids = list(range(max(1, last_message_id - batch_size), last_message_id))
            messages = await client.get_messages(CHANNEL_ID, message_ids)

            video_entries = [
                {"message_id": msg.id}
                for msg in messages if msg and msg.video and not collection.find_one({"message_id": msg.id})
            ]

            if video_entries:
                collection.insert_many(video_entries)  # ✅ Bulk insert for efficiency
                indexed_count += len(video_entries)

            last_message_id -= batch_size
        except Exception as e:
            logger.error(f"Error during indexing: {e}")
            break  # ✅ Exit loop on error to prevent API spam

    if indexed_count > 0:
        await message.reply_text(f"✅ Indexing completed! {indexed_count} videos added.")
        await client.send_message(OWNER_ID, f"📢 Successfully indexed {indexed_count} videos!")
    else:
        await message.reply_text("⚠ No new videos found!")

# 🔰 Start Command with Inline Button
@bot.on_message(filters.command("start"))
async def start(client, message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎥 Get Random Video", callback_data="get_random_video")]
    ])
    await message.reply_text("Welcome! Click the button below to get a random video:", reply_markup=keyboard)

# 🔰 Callback for Random Video
@bot.on_callback_query(filters.regex("get_random_video"))
async def random_video_callback(client, callback_query: CallbackQuery):
    await send_random_video(client, callback_query.message.chat.id)
    await callback_query.answer()

# 🔰 Run the Bot
if __name__ == "__main__":
    threading.Thread(target=start_health_check, daemon=True).start()
    bot.run()
