from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

HELP_TEXT = """📌 **Bot Usage Guide**:
- 🎥 Click the "Get Random Video" button to receive a random video.
- 🗑️ The video auto-deletes after a set time.
- 📊 You have a limited quota of videos per 6 hours.
- 🎁 Invite friends to earn extra quota!

⚠️ **Disclaimer**:
- 🚫 We do not store videos permanently.
- 🔞 Content is user-uploaded, use at your own risk.

✅ **Rules**:
1️⃣ No spamming commands.
2️⃣ Don't misuse the bot.

"""

@Client.on_callback_query(filters.regex("show_help"))
async def show_help(client, query: CallbackQuery):
    buttons = InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close", callback_data="close")]])
    await query.message.edit_text(HELP_TEXT, reply_markup=buttons)

@Client.on_callback_query(filters.regex("close"))
async def close_help(client, query: CallbackQuery):
    await query.message.delete()
