import logging
from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN
from handlers import start, random_video, index, delete_video, stats, quota, my_plan, broadcast

# Configure logging
logging.basicConfig(level=logging.INFO)

bot = Client("RandomVideoBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Register handlers
bot.add_handler(start.handler)
bot.add_handler(random_video.handler)
bot.add_handler(index.handler)
bot.add_handler(delete_video.handler)
bot.add_handler(stats.handler)
bot.add_handler(quota.handler)
bot.add_handler(my_plan.my_plan_handler)
bot.add_handler(broadcast.handler)

if __name__ == "__main__":
    bot.run()
