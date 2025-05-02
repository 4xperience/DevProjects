import aiohttp
import redis.asyncio as redis
from src.core.config import settings

CACHE_KEY = "usd_rate"
CACHE_TTL = 300

def get_redis_client():
    return redis.from_url(settings.REDIS_URL, decode_responses=True)

async def get_usd_rate() -> float:
    redis_client = get_redis_client()

    cached = await redis_client.get(CACHE_KEY)
    if cached:
        return float(cached)

    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.cbr-xml-daily.ru/daily_json.js") as resp:
            data = await resp.json(content_type=None)
            rate = data["Valute"]["USD"]["Value"]

            await redis_client.set(CACHE_KEY, rate, ex=CACHE_TTL)
            return float(rate)
