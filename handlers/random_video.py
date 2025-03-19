from pyrogram import Client, filters
from pyrogram.types import Message
from database.video_management import get_random_video, increment_video_usage, check_quota

@Client.on_message(filters.command("random"))
async def handler(client, message: Message):
    user_id = message.from_user.id
    if not check_quota(user_id):
        await message.reply_text("Your quota is exhausted! Refer friends to renew.")
        return

    video = get_random_video()
    if video:
        await client.send_video(message.chat.id, video['file_id'], caption="Here’s a random video! 🎥")
        increment_video_usage(user_id)
    else:
        await message.reply_text("No videos available in the database.")
