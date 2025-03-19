from pyrogram import Client, filters
from database import delete_video

@Client.on_message(filters.command("delete_video") & filters.user(OWNER_ID))
async def delete_video_command(client, message):
    if not message.reply_to_message or not message.reply_to_message.video:
        await message.reply_text("❌ Reply to a video to delete it.")
        return

    file_id = message.reply_to_message.video.file_id
    if await delete_video(file_id):
        await message.reply_text("🗑️ Video deleted successfully!")
    else:
        await message.reply_text("⚠️ Video not found in database.")
