from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING
from pymongo.errors import DuplicateKeyError
from config import MONGO_URI, DATABASE_NAME  # Importing from config

# Database connection setup
client = AsyncIOMotorClient(MONGO_URI)
db = client[DATABASE_NAME]

# Ensure indexes for efficiency
async def create_indexes():
    await db.users.create_index([("user_id", ASCENDING)], unique=True)

# Initialize the database
async def init_db():
    await create_indexes()

# Add a new user to the database
async def add_user(user_id: int, username: str):
    try:
        user = {"user_id": user_id, "username": username, "plan": "free"}
        await db.users.insert_one(user)
    except DuplicateKeyError:
        print(f"User {user_id} already exists!")

# Get a user's data by user_id
async def get_user(user_id: int):
    return await db.users.find_one({"user_id": user_id})

# Get all users in the database
async def get_all_users():
    return await db.users.find().to_list(length=None)

# Update a user's subscription plan
async def update_user_plan(user_id: int, plan: str):
    await db.users.update_one({"user_id": user_id}, {"$set": {"plan": plan}})

# Get the user's subscription plan
async def get_user_plan(user_id: int):
    user = await get_user(user_id)
    return user.get("plan", None) if user else None

# Set a user as premium
async def set_premium(user_id: int, plan: str = "premium"):
    await update_user_plan(user_id, plan)

# Check if a user is premium
async def is_premium(user_id: int):
    plan = await get_user_plan(user_id)
    return plan == "premium"

# Remove a user from premium
async def remove_premium(user_id: int):
    await update_user_plan(user_id, "free")

# Get the number of premium users
async def count_premium_users():
    return await db.users.count_documents({"plan": "premium"})

# Reset all users' plans to free
async def reset_all_users():
    await db.users.update_many({}, {"$set": {"plan": "free"}})
