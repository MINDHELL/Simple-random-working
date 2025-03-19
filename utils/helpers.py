from pyrogram.types import Message

async def send_welcome_message(client, message: Message):
    await message.reply_photo("assets/welcome.jpg", caption="Welcome! Read the rules before using the bot.")
