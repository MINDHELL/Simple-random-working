from pyrogram import Client, filters
from database import get_total_videos, get_total_users

@Client.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def stats_command(client, message):
    users_count = await get_total_users()
    videos_count = await get_total_videos()

    await message.reply_text(
        f"📊 **Bot Statistics:**\n\n👥 Users: {users_count}\n📂 Indexed Videos: {videos_count}"
    )

@Client.on_message(filters.command("files") & filters.user(OWNER_ID))
async def files_command(client, message):
    count = await get_total_videos()
    await message.reply_text(f"📂 **Total Indexed Videos:** {count}")
