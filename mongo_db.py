from pymongo import MongoClient
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os
import certifi

load_dotenv()

username = quote_plus(os.getenv("MONGO_USER"))
password = quote_plus(os.getenv("MONGO_PASS"))
cluster = os.getenv("MONGO_CLUSTER")

uri = f"mongodb+srv://{username}:{password}@{cluster}/mental_health?retryWrites=true&w=majority"

try:
    client = MongoClient(
        uri,
        tls=True,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=5000,
        socketTimeoutMS=5000
    )

    client.admin.command("ping")
    print("✅ MongoDB Connected")

except Exception as e:
    print("❌ MongoDB Connection Failed:", e)
    client = None

if client:
    db = client["mental_health"]

    users_collection = db["users"]
    chats_collection = db["chats"]
    messages_collection = db["messages"]