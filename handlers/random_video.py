import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from database.video_management import get_random_video, increment_video_usage, check_quota

# Configure logging
logging.basicConfig(level=logging.INFO)

@Client.on_message(filters.command("random"))
async def random_video_handler(client, message: Message):
    user_id = message.from_user.id

    try:
        # Check if the user has quota left
        if not check_quota(user_id):
            await message.reply_text("❌ Your quota is exhausted! Refer friends to renew.")
            return

        # Fetch a random video from the database
        video = get_random_video()
        if video:
            await client.send_video(
                message.chat.id, 
                video['file_id'], 
                caption="🎥 Here’s a random video!"
            )
            increment_video_usage(user_id)  # Update the user's quota usage
            logging.info(f"Sent a random video to user {user_id}")
        else:
            await message.reply_text("⚠️ No videos available in the database.")
            logging.warning(f"User {user_id} requested a video, but database is empty.")

    except Exception as e:
        logging.error(f"Error sending random video to user {user_id}: {e}")
        await message.reply_text("⚠️ An error occurred while retrieving a video. Please try again later.")

# Ensure the handler is registered correctly
handler = random_video_handler
