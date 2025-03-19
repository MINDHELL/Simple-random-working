from pyrogram import Client, filters
from database import add_video

@Client.on_message(filters.video & filters.user(OWNER_ID))
async def index_video(client, message):
    file_id = message.video.file_id
    if await add_video(file_id):
        await message.reply_text("✅ Video indexed successfully!")
    else:
        await message.reply_text("⚠️ Duplicate video detected. Skipping...")
