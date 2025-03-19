from pyrogram import Client, filters
from pyrogram.types import Message
from database import get_all_users
from config import OWNER_ID

@Client.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast_handler(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("⚠️ Reply to a message to broadcast.")

    users = get_all_users()
    sent_count = 0
    failed_count = 0

    for user in users:
        try:
            await client.send_message(user, message.reply_to_message.text)
            sent_count += 1
        except:
            failed_count += 1

    await message.reply_text(f"📢 *Broadcast Report:*\n✅ Sent: {sent_count}\n❌ Failed: {failed_count}", parse_mode="markdown")
