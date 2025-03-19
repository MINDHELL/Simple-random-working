from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from utils.helpers import send_welcome_message

# Disclaimer & Rules Text
DISCLAIMER_TEXT = "⚠️ *Disclaimer:* \n\nBy using this bot, you agree that the content is for educational purposes only."
RULES_TEXT = "📜 *Rules:* \n\n1️⃣ Do not spam the bot. \n2️⃣ Respect others. \n3️⃣ No illegal requests."

# Start Handler
@Client.on_message(filters.command("start"))
async def handler(client, message: Message):
    # Send Welcome Message with Image
    await client.send_photo(
        message.chat.id,
        "assets/welcome.jpg",
        caption="👋 Welcome! Read the disclaimer & rules before using the bot.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📜 Disclaimer", callback_data="show_disclaimer")],
            [InlineKeyboardButton("⚖️ Rules", callback_data="show_rules")],
        ])
    )

# Callback Query Handler for Disclaimer & Rules
@Client.on_callback_query()
async def callback_handler(client, query):
    if query.data == "show_disclaimer":
        await query.message.edit_text(
            DISCLAIMER_TEXT,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("❌ Close", callback_data="close")]
            ])
        )
    elif query.data == "show_rules":
        await query.message.edit_text(
            RULES_TEXT,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("❌ Close", callback_data="close")]
            ])
        )
    elif query.data == "close":
        await query.message.delete()
