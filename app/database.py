import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from .config import MONGODB_URL, DB_NAME

# Update connection with explicit TLS options and server selection timeout
client = AsyncIOMotorClient(
    MONGODB_URL,
    tlsCAFile=certifi.where(),
    ssl=True,
    ssl_cert_reqs="CERT_REQUIRED",
    serverSelectionTimeoutMS=30000,
    connectTimeoutMS=30000
)
db = client[DB_NAME]