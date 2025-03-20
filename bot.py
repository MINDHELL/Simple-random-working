import asyncio
import logging
from aiohttp import web
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
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

# Add handlers
bot.add_handler(start.handler)
bot.add_handler(random_video.handler)
bot.add_handler(index.handler)
bot.add_handler(delete_video.handler)
bot.add_handler(stats.handler)
bot.add_handler(quota.handler)
bot.add_handler(my_plan.handler)
bot.add_handler(broadcast.handler)

# Run both the bot and the web server
async def main():
    async with bot:  # Ensure proper startup and shutdown of Pyrogram bot
        await asyncio.gather(
            start_web_server(),  # Start the health check server
            bot.run()  # Start the Telegram bot properly
        )

if __name__ == "__main__":
    asyncio.run(main())
