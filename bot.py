import asyncio
import logging
from aiohttp import web
from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID
from handlers.start import start_command_handler
from handlers.stats import stats_handler
from handlers import random_video, index, delete_video, quota, my_plan, broadcast

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize Pyrogram bot
bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Dummy health check server for Koyeb
async def health_check(request):
    return web.Response(text="OK")

async def start_web_server():
    try:
        app = web.Application()
        app.router.add_get("/", health_check)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", 8080)
        await site.start()
        logging.info("✅ Health check server running on port 8080")
    except Exception as e:
        logging.error(f"❌ Web server error: {e}")

# Add handlers correctly
def add_handlers():
    try:
        bot.add_handler(start_command_handler)
        bot.add_handler(random_video_handler)
        bot.add_handler(index.handler)
        bot.add_handler(delete_video_handler)
        bot.add_handler(stats_handler)
        bot.add_handler(quota_handler)
        bot.add_handler(my_plan_handler)
        bot.add_handler(broadcast.handler)
        logging.info("✅ Handlers added successfully!")
    except Exception as e:
        logging.error(f"❌ Error adding handlers: {e}")

async def send_startup_message():
    try:
        await bot.send_message(OWNER_ID, "✅ Bot is successfully deployed and running!")
        logging.info("✅ Startup message sent to owner.")
    except Exception as e:
        logging.error(f"❌ Failed to send startup message: {e}")

async def main():
    try:
        logging.info("🚀 Starting bot...")
        add_handlers()  # Add handlers before starting bot
        await bot.start()  # Start bot
        logging.info("✅ Bot started successfully!")
        
        await send_startup_message()  # Notify owner bot is running
        await start_web_server()  # Start web server
        
        logging.info("✅ Bot is running. Waiting for commands...")
        await idle()  # Keep bot running

    except Exception as e:
        logging.error(f"❌ Critical Error: {e}")

    finally:
        await bot.stop()
        logging.info("🛑 Bot stopped.")

if __name__ == "__main__":
    asyncio.run(main())  # Proper event loop handling
