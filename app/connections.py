from system_config import DB
from databases import Database
from redis import asyncio as aioredis

db = Database(DB.POSTGRES_URL)
redis = None

#return database
def get_db():
    return db

#connect to database 
async def connect_to_db():
    await get_db().connect()

#disconnect from database
async def disconnect_from_db():
    await get_db().disconnect()

#connect to redis
async def connect_to_redis():
    global redis
    redis = aioredis.from_url(DB.REDIS_URL)

#disconnect from redis
async def disconnect_from_redis():
    redis.close()