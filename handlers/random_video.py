from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup
from database import get_random_video, increment_video_usage, check_quota

@Client.on_message(filters.text & filters.private)
async def random_video_handler(client, message):
    user_id = message.from_user.id

    if not await check_quota(user_id):
        await message.reply_text("🚫 You've reached your video limit. Try again later!")
        return

    video = await get_random_video()
    if video:
        await message.reply_video(video['file_id'], caption="🎥 Here's your random video!")
        await increment_video_usage(user_id)
    else:
        await message.reply_text("❌ No videos found!")

# Add the "Get Random Video" button
random_video_button = ReplyKeyboardMarkup([["🎥 Get Random Video"]], resize_keyboard=True)
