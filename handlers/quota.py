import logging
from pyrogram import Client, filters
from config import OWNER_ID
from pyrogram.types import Message
from database.video_management import check_quota, reset_quota

# Configure logging
logging.basicConfig(level=logging.INFO)

@Client.on_message(filters.command("quota"))
async def quota_handler(client, message: Message):
    try:
        user_id = message.from_user.id
        remaining = check_quota(user_id)

        if remaining is None:
            response = "⚠️ Unable to retrieve your quota. Please try again later."
        else:
            response = f"📊 *Your Quota:* \n🔹 You have {remaining} videos left today."

        await message.reply_text(response, parse_mode="markdown")

    except Exception as e:
        logging.error(f"Error checking quota for user {user_id}: {e}")
        await message.reply_text("⚠️ An error occurred while retrieving your quota. Please try again later.")

@Client.on_message(filters.command("reset_quota") & filters.user(OWNER_ID))
async def reset_quota_handler(client, message: Message):
    try:
        reset_quota()
        await message.reply_text("✅ All user quotas have been reset successfully.")
        logging.info("User quotas reset by admin.")

    except Exception as e:
        logging.error(f"Error resetting quotas: {e}")
        await message.reply_text("⚠️ Failed to reset quotas. Please try again later.")

# Ensure handlers are registered properly
quota_handler = quota_handler
reset_quota_handler = reset_quota_handler
handler = quota_handler  # Replace function_name with the actual command handler
