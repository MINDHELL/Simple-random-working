from pyrogram import Client, filters
from database import get_all_users
import asyncio

@Client.on_message(filters.command("broadcast") & filters.user(OWNER_ID) & filters.reply)
async def broadcast_command(client, message):
    users = await get_all_users()
    broadcast_message = message.reply_to_message
    count = 0

    for user in users:
        try:
            await broadcast_message.copy(chat_id=user["id"])
            count += 1
            await asyncio.sleep(0.5)
        except:
            pass

    await message.reply_text(f"📢 Broadcast sent to {count} users!")
