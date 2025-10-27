from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "notes_api")

client: AsyncIOMotorClient = None

async def connect_to_mongo():
    global client
    try:
        client = AsyncIOMotorClient(MONGO_URL)
        # Test the connection
        await client.admin.command('ping')
        print("Connected to MongoDB")
    except ServerSelectionTimeoutError as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise

async def close_mongo_connection():
    global client
    if client:
        client.close()
        print("Disconnected from MongoDB")

def get_database():
    return client[DATABASE_NAME]

def get_collection(collection_name: str):
    return get_database()[collection_name]