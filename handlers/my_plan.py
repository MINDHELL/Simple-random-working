import asyncio
from datetime import datetime, timedelta
from pyrogram import Client, filters
from database import db

# Command: /myplan
@Client.on_message(filters.command("myplan"))
async def my_plan(client, message):
    user_id = message.from_user.id
    user_data = await db.get_user(user_id)

    if not user_data:
        return await message.reply("You are not registered in the database.")

    quota = user_data.get("quota", 0)
    last_reset = user_data.get("last_reset")

    # Convert last_reset timestamp to datetime
    if last_reset:
        last_reset_time = datetime.fromtimestamp(last_reset)
        next_reset_time = last_reset_time + timedelta(hours=6)
        time_left = next_reset_time - datetime.now()

        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        reset_msg = f"Next quota renewal in {hours} hours, {minutes} minutes."
    else:
        reset_msg = "Quota renewal time unavailable."

    # Check referral bonus
    referrals = user_data.get("referrals", 0)
    referral_msg = f"You have referred {referrals}/5 users. Refer 5 users to reset your quota early!"

    # Response message
    response = (
        f"🎟 **Your Plan Details** 🎟\n\n"
        f"📌 **Videos Left:** `{quota}/20`\n"
        f"⏳ {reset_msg}\n\n"
        f"🎁 {referral_msg}"
    )

    await message.reply(response)
