import time
import logging
from pyrogram.types import Message

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def send_welcome_message(client, message: Message):
    """Sends a welcome message with a photo."""
    try:
        await message.reply_photo("assets/welcome.jpg", caption="Welcome! Read the rules before using the bot.")
        logger.info(f"✅ Welcome message sent to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"❌ Error sending welcome message: {e}")

def format_time(seconds: int) -> str:
    """Converts seconds to HH:MM:SS format."""
    try:
        return time.strftime("%H:%M:%S", time.gmtime(seconds))
    except Exception as e:
        logger.error(f"❌ Error formatting time: {e}")
        return "00:00:00"  # Default fallback

def human_readable_size(size: int) -> str:
    """Converts file size into a human-readable format."""
    try:
        if size < 1024:
            return f"{size} B"
        elif size < 1024**2:
            return f"{size/1024:.2f} KB"
        elif size < 1024**3:
            return f"{size/1024**2:.2f} MB"
        else:
            return f"{size/1024**3:.2f} GB"
    except Exception as e:
        logger.error(f"❌ Error formatting size: {e}")
        return "Unknown Size"  # Default fallback
