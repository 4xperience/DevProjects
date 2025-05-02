from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings

mongo_client = AsyncIOMotorClient(settings.MONGO_URL)
mongo_db = mongo_client["delivery"]
logs_collection = mongo_db["delivery_logs"]
