import asyncio
import os

import aioredis
from loguru import logger


async def check_redis():
    try:
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = os.getenv("REDIS_PORT", "6379")
        redis_url = f"redis://{redis_host}:{redis_port}"
        redis = await aioredis.from_url(redis_url)
        response = await redis.ping()
        if response:
            logger.info("Redis is running")
        else:
            logger.info("Redis is not running")
    except aioredis.ConnectionError:
        logger.info("Cannot connect to Redis")


if __name__ == "__main__":
    asyncio.run(check_redis())
