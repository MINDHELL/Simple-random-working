import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from database.db import get_all_users
from config import OWNER_ID

@Client.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast_handler(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("⚠️ Reply to a message to broadcast.")

    users = await get_all_users()
    sent_count = 0
    failed_count = 0

    for user in users:
        try:
            await client.send_message(user["user_id"], message.reply_to_message.text)
            sent_count += 1
        except Exception as e:
            logging.error(f"Failed to send message to {user['user_id']}: {e}")
            failed_count += 1

    report = f"📢 *Broadcast Report:*\n✅ Sent: {sent_count}\n❌ Failed: {failed_count}"
    await message.reply_text(report, parse_mode="markdown")

handler = broadcast_handler
