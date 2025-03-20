import asyncio
import logging
from aiohttp import web
from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID
from handlers import start, random_video, index, delete_video, stats, quota, my_plan, broadcast

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize Pyrogram bot
bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Dummy health check server for Koyeb
async def health_check(request):
    return web.Response(text="OK")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    logging.info("Health check server running on port 8080")

# Add handlers correctly
def add_handlers():
    bot.add_handler(start.handler)
    bot.add_handler(random_video.handler)
    bot.add_handler(index.handler)
    bot.add_handler(delete_video.handler)
    bot.add_handler(stats.handler)
    bot.add_handler(quota.handler)
    bot.add_handler(my_plan.handler)
    bot.add_handler(broadcast.handler)

async def send_startup_message():
    try:
        await bot.send_message(OWNER_ID, "✅ Bot is successfully deployed and running!")
        logging.info("Startup message sent to owner.")
    except Exception as e:
        logging.error(f"Failed to send startup message: {e}")

async def main():
    add_handlers()  # Add handlers before starting bot
    await bot.start()  # Start bot
    await send_startup_message()  # Notify owner bot is running
    await start_web_server()  # Start web server
    logging.info("Bot is running...")

    try:
        await idle()  # Keep bot running
    except Exception as e:
        logging.error(f"Error in idle: {e}")
    finally:
        await bot.stop()
        logging.info("Bot stopped.")

if __name__ == "__main__":
    asyncio.run(main())  # Proper event loop handling
