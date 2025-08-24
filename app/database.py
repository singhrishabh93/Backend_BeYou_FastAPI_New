from motor.motor_asyncio import AsyncIOMotorClient
from .config import MONGODB_URL, DB_NAME

# Simplified connection - MongoDB Atlas handles SSL/TLS automatically
client = AsyncIOMotorClient(MONGODB_URL)
db = client[DB_NAME]