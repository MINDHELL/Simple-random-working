from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

OWNER_USERNAME = "@cosmos6t"

async def start_command(client, message):
    welcome_text = "👋 **Welcome to Random Video Bot!**\n\n⚡ Get random videos instantly!\n\n📜 **Rules & Disclaimer:** Tap below!"
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("👑 Owner", url=f"https://t.me/{OWNER_USERNAME}")],
        [InlineKeyboardButton("ℹ️ Help & Rules", callback_data="show_help")]
    ])
    
    await message.reply_photo(
        photo="https://envs.sh/nek.jpg",  # Add a valid welcome image
        caption=welcome_text,
        reply_markup=buttons
    )

@Client.on_message(filters.command("start"))
async def handler(client, message):
    await start_command(client, message)
