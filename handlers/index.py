import logging
from pyrogram import Client, filters
from config import OWNER_ID
from pyrogram.types import Message
from database.video_management import index_video

@Client.on_message(filters.command("index") & filters.user(OWNER_ID))
async def handler(client, message: Message):
    try:
        if not message.reply_to_message or not message.reply_to_message.video:
            await message.reply_text("⚠️ Please reply to a video to index it.")
            return
        
        video_file_id = message.reply_to_message.video.file_id
        response = index_video(video_file_id)
        
        if response:
            await message.reply_text(f"✅ Video indexed successfully!")
        else:
            await message.reply_text("❌ Failed to index the video. It might already be indexed.")

    except Exception as e:
        logging.error(f"Error indexing video: {e}")
        await message.reply_text("⚠️ An error occurred while indexing the video.")

handler = handler
