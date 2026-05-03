"""
Chat database operations module.
Handles chat creation, retrieval, and management operations.
"""

from datetime import datetime
from database import get_chats_collection, get_messages_collection
from logger import setup_logger

logger = setup_logger(__name__)

# ================= CREATE NEW CHAT =================
def create_chat(user_id, chat_id, title):
    chats_collection = get_chats_collection()
    chats_collection.insert_one({
        "user_id": user_id,
        "chat_id": chat_id,
        "title": title,
        "created_at": datetime.utcnow()
    })

# ================= SAVE MESSAGE =================
def save_message(user_id, chat_id, role, content):
    messages_collection = get_messages_collection()
    messages_collection.insert_one({
        "user_id": user_id,
        "chat_id": chat_id,
        "role": role,
        "content": content,
        "timestamp": datetime.utcnow()
    })

# ================= LOAD CHAT =================
def load_chat(user_id, chat_id):
    messages_collection = get_messages_collection()
    messages = messages_collection.find(
        {
            "user_id": user_id,
            "chat_id": chat_id
        }
    ).sort("timestamp", 1)

    chat_list = []
    for m in messages:
        chat_list.append({
            "role": m["role"],
            "content": m["content"]
        })

    return chat_list

# ================= GET USER CHATS =================
def get_user_chats(user_id):
    chats_collection = get_chats_collection()
    chats = chats_collection.find(
        {"user_id": user_id}
    ).sort("created_at", -1)

    return list(chats)

# ================= DELETE CHAT =================
def delete_chat(user_id, chat_id):
    chats_collection = get_chats_collection()
    messages_collection = get_messages_collection()
    
    chats_collection.delete_one({
        "user_id": user_id,
        "chat_id": chat_id
    })

    messages_collection.delete_many({
        "user_id": user_id,
        "chat_id": chat_id
    })

# ================= RENAME CHAT =================
def rename_chat(user_id, chat_id, new_title):
    chats_collection = get_chats_collection()
    chats_collection.update_one(
        {
            "user_id": user_id,
            "chat_id": chat_id
        },
        {
            "$set": {"title": new_title}
        }
    )