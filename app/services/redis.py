import redis.asyncio as redis
from fastapi import Depends

redis_client = None

async def connect_redis():
    global redis_client
    redis_client = redis.from_url("redis://localhost", decode_responses=True)
    return redis_client

async def get_redis() -> redis.Redis:
    return redis_client