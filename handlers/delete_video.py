from pyrogram import Client, filters
from pyrogram.types import Message
from database.video_management import delete_video

@Client.on_message(filters.command("delete_video") & filters.user(OWNER_ID))
async def handler(client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.video:
        await message.reply_text("Reply to a video to delete it.")
        return
    
    video_file_id = message.reply_to_message.video.file_id
    response = delete_video(video_file_id)
    await message.reply_text(response)
