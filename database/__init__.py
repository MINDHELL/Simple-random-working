from .db import db

user_collection = db["Users"]  # Ensure your database has a Users collection

def get_user_plan(user_id):
    user = user_collection.find_one({"user_id": user_id})
    return user.get("plan", "Free") if user else "Free"  # Default to "Free" plan
