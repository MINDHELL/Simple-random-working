from pyrogram import Client, filters
from pyrogram.types import Message
from database.video_management import get_video_count

@Client.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def handler(client, message: Message):
    count = get_video_count()
    await message.reply_text(f"Total videos in database: {count}")
