from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN
from handlers import start, random_video, index, delete_video, stats, quota, my_plan, broadcast
from database import init_db

# Initialize bot
bot = Client("RandomVideoBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Initialize database
init_db()

# Register handlers
bot.add_handler(start.handler)
bot.add_handler(random_video.handler)
bot.add_handler(index.handler)
bot.add_handler(delete_video.handler)
bot.add_handler(stats.handler)
bot.add_handler(quota.handler)
bot.add_handler(my_plan.handler)
bot.add_handler(broadcast.handler)

# Start bot
print("Bot is running...")
bot.run()
