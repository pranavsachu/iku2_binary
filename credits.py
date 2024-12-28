import os
import json
from database import update_user_credits


CREDITS_FILE = "credits.json"

def get_credits():
    if not os.path.exists(CREDITS_FILE):
        return 0
    with open(CREDITS_FILE, "r") as file:
        data = json.load(file)
        return data.get("credits", 0)

from database import get_user_credits, update_user_credits

def add_credits(user_id, amount):
    current_credits = get_user_credits(user_id)
    new_credits = current_credits + amount
    update_user_credits(user_id, new_credits)
    print(f"Updated credits for user {user_id}: {new_credits}")

def get_credits(user_id):
    return get_user_credits(user_id)

