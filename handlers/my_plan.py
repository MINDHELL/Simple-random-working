import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from database import get_user_plan

# Configure logging
logging.basicConfig(level=logging.INFO)

async def my_plan_handler(client, message: Message):
    try:
        user_id = message.from_user.id
        plan_info = await get_user_plan(user_id)

        if plan_info:
            response = (
                f"📜 *Your Plan Details:* \n\n"
                f"🔹 **Plan Type:** {plan_info.get('plan_type', 'Unknown')}\n"
                f"⏳ **Expiry Date:** {plan_info.get('expiry', 'N/A')}\n"
                f"📦 **Quota Left:** {plan_info.get('quota', '0')} videos\n"
            )
        else:
            response = "❌ You don't have an active plan. Use /subscription to buy one."

        await message.reply_text(response, parse_mode="markdown")

    except Exception as e:
        logging.error(f"Error fetching user plan: {e}")
        await message.reply_text("⚠️ An error occurred while retrieving your plan details. Please try again later.")

# Register the command properly
handler = Client.on_message(filters.command("my_plan"))(my_plan_handler)
