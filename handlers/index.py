from pyrogram import Client, filters
from config import OWNER_ID
from pyrogram.types import Message
from database.video_management import index_video

@Client.on_message(filters.command("index") & filters.user(OWNER_ID))
async def handler(client, message: Message):
    if message.video:
        video_file_id = message.video.file_id
        response = index_video(video_file_id)
        await message.reply_text(response)
    else:
        await message.reply_text("Please send a video with this command!")
