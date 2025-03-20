import logging
from pyrogram import Client, filters
from config import OWNER_ID
from pyrogram.types import Message
from database.video_management import delete_video

@Client.on_message(filters.command("delete_video") & filters.user(OWNER_ID))
async def handler(client, message: Message):
    try:
        if not message.reply_to_message or not message.reply_to_message.video:
            await message.reply_text("⚠️ Reply to a video to delete it.")
            return
        
        video_file_id = message.reply_to_message.video.file_id
        response = delete_video(video_file_id)
        
        if response:
            await message.reply_text(f"✅ Video deleted successfully!")
        else:
            await message.reply_text("❌ Video not found in the database.")
    except Exception as e:
        logging.error(f"Error deleting video: {e}")
        await message.reply_text("⚠️ An error occurred while deleting the video.")

handler = handler
