import random
import logging
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup
from pymongo import MongoClient

# ✅ Logging setup
logging.basicConfig(level=logging.INFO)

# ✅ Your API variables
API_ID = 22295141
API_HASH = "94f465fa81e524caed32759c66bcb1b2"
BOT_TOKEN = "6375581346:AAEmYrYqOPP-sHvXhDgMyviAHD4q8bw1xLU"
MONGO_URI = "mongodb+srv://root:root@cluster0.hkmjddt.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "video_bot"
COLLECTION_NAME = "videos"
CHANNEL_ID = -1002130948292  # ✅ Your Telegram channel ID
OWNER_ID = 5147480370  # ✅ Your Telegram user ID

# ✅ Initialize bot
bot = Client("video_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ✅ Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# ✅ ReplyKeyboard Markup
keyboard = ReplyKeyboardMarkup([["🎥 Get Random Video"]], resize_keyboard=True)

# ✅ Start Command
@bot.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text("👋 Welcome! Click below to get a random video.", reply_markup=keyboard)

# ✅ Index Command (Admin Only)
@bot.on_message(filters.command("index") & filters.user(OWNER_ID))
async def index_videos(client, message):
    await message.reply_text("🔄 Indexing videos... Please wait.")

    indexed_count = 0
    async for msg in client.get_chat_history(CHANNEL_ID, limit=1000):
        if msg.video:
            collection.update_one(
                {"message_id": msg.id},
                {"$set": {
                    "message_id": msg.id,
                    "file_id": msg.video.file_id  # ✅ Save file_id
                }},
                upsert=True
            )
            indexed_count += 1

    await message.reply_text(f"✅ Indexing completed! {indexed_count} videos added.")

# ✅ Send Random Video
async def send_random_video(client, chat_id):
    video_docs = list(collection.find())
    if not video_docs:
        await client.send_message(chat_id, "⚠ No videos available. Use /index first!")
        return

    random_video = random.choice(video_docs)

    if "file_id" in random_video:
        await client.send_video(chat_id, video=random_video["file_id"])
    else:
        await client.forward_messages(chat_id, from_chat_id=CHANNEL_ID, message_ids=random_video["message_id"])

# ✅ Handle "Get Random Video" button
@bot.on_message(filters.text & filters.private)
async def handle_buttons(client, message):
    if message.text == "🎥 Get Random Video":
        await send_random_video(client, message.chat.id)

# ✅ Run the Bot
bot.run()
