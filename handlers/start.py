import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from utils.helpers import send_welcome_message

# Configure logging
logging.basicConfig(level=logging.INFO)

# Disclaimer & Rules Text
DISCLAIMER_TEXT = "⚠️ *Disclaimer:* \n\nBy using this bot, you agree that the content is for educational purposes only."
RULES_TEXT = "📜 *Rules:* \n\n1️⃣ Do not spam the bot. \n2️⃣ Respect others. \n3️⃣ No illegal requests."

# Start Command Handler
@Client.on_message(filters.command("start"))
async def start_handler(client: Client, message: Message):
    try:
        # Send Welcome Message with Inline Buttons
        await client.send_photo(
            message.chat.id,
            "assets/welcome.jpg",
            caption="👋 Welcome! Read the disclaimer & rules before using the bot.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📜 Disclaimer", callback_data="show_disclaimer")],
                [InlineKeyboardButton("⚖️ Rules", callback_data="show_rules")],
            ])
        )
        logging.info(f"Sent welcome message to user {message.from_user.id}")
    except Exception as e:
        logging.error(f"Error sending welcome message to {message.from_user.id}: {e}")
        await message.reply_text("⚠️ Unable to send welcome message. Please try again.")

# Callback Query Handler for Inline Buttons
@Client.on_callback_query()
async def callback_handler(client: Client, query: CallbackQuery):
    try:
        if query.data == "show_disclaimer":
            await query.message.edit_text(
                DISCLAIMER_TEXT,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close", callback_data="close")]])
            )
        elif query.data == "show_rules":
            await query.message.edit_text(
                RULES_TEXT,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close", callback_data="close")]])
            )
        elif query.data == "close":
            await query.message.delete()
        
        logging.info(f"Handled callback query: {query.data} for user {query.from_user.id}")

    except Exception as e:
        logging.error(f"Error handling callback query ({query.data}) for user {query.from_user.id}: {e}")
        await query.answer("⚠️ Something went wrong. Please try again.")
