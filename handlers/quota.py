from pyrogram import Client, filters
from database import get_remaining_quota, reset_quota, increase_quota_by_referral

@Client.on_message(filters.command("my_plan"))
async def my_plan_command(client, message):
    user_id = message.from_user.id
    remaining_quota, reset_time = await get_remaining_quota(user_id)

    await message.reply_text(
        f"🎟️ **Your Plan:**\n\n📊 Videos Left: {remaining_quota}\n⏳ Reset In: {reset_time}"
    )

@Client.on_message(filters.command("refer"))
async def referral_command(client, message):
    user_id = message.from_user.id
    if await increase_quota_by_referral(user_id):
        await message.reply_text("🎉 Referral successful! Your quota has been renewed.")
    else:
        await message.reply_text("❌ You need more referrals to renew your quota.")
