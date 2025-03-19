from pyrogram.types import Message

async def send_welcome_message(client, message: Message):
    await message.reply_photo("assets/welcome.jpg", caption="Welcome! Read the rules before using the bot.")

import time

def format_time(seconds: int) -> str:
    """Converts seconds to HH:MM:SS format."""
    return time.strftime("%H:%M:%S", time.gmtime(seconds))

def human_readable_size(size: int) -> str:
    """Converts file size into human-readable format."""
    if size < 1024:
        return f"{size} B"
    elif size < 1024**2:
        return f"{size/1024:.2f} KB"
    elif size < 1024**3:
        return f"{size/1024**2:.2f} MB"
    else:
        return f"{size/1024**3:.2f} GB"
