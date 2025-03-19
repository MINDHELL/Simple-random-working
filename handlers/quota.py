from pyrogram import Client, filters
from pyrogram.types import Message
from database.video_management import check_quota, reset_quota

@Client.on_message(filters.command("quota"))
async def handler(client, message: Message):
    user_id = message.from_user.id
    remaining = check_quota(user_id)
    await message.reply_text(f"You have {remaining} videos left today.")

@Client.on_message(filters.command("reset_quota") & filters.user(OWNER_ID))
async def handler(client, message: Message):
    reset_quota()
    await message.reply_text("All user quotas have been reset.")
