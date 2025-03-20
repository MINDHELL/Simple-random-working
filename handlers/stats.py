import logging
from pyrogram import Client, filters
from config import OWNER_ID
from pyrogram.types import Message
from database.video_management import get_video_count

# Configure logging
logging.basicConfig(level=logging.INFO)

@Client.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def stats_handler(client: Client, message: Message):
    try:
        count = get_video_count()
        await message.reply_text(f"📊 *Database Stats:*\n\n🎥 Total videos: {count}", parse_mode="markdown")
        logging.info(f"Stats command used by {message.from_user.id}. Total videos: {count}")
    except Exception as e:
        logging.error(f"Error fetching video count for user {message.from_user.id}: {e}")
        await message.reply_text("⚠️ Unable to fetch database stats. Please try again later.")
