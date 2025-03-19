from pyrogram import Client, filters
from pyrogram.types import Message
from database import get_user_plan

@Client.on_message(filters.command("my_plan"))
async def my_plan_handler(client, message: Message):
    user_id = message.from_user.id
    plan_info = get_user_plan(user_id)

    if plan_info:
        response = (
            f"📜 *Your Plan Details:* \n\n"
            f"🔹 **Plan Type:** {plan_info['plan_type']}\n"
            f"⏳ **Expiry Date:** {plan_info['expiry']}\n"
            f"📦 **Quota Left:** {plan_info['quota']} videos\n"
        )
    else:
        response = "❌ You don't have an active plan. Use /subscription to buy one."

    await message.reply_text(response, parse_mode="markdown")
