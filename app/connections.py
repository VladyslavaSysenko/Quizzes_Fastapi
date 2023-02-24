from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])
from system_config import DB
sys.path.pop(0)

from databases import Database
from redis import asyncio as aioredis

db = Database(DB.POSTGRES_URL)
redis=None
REDIS_URL = "redis://redis"

#connect to database 
async def connect_to_db():
    await db.connect()

#disconnect from database
async def disconnect_from_db():
    await db.disconnect()

#connect to redis
async def connect_to_redis():
    global redis
    redis = aioredis.from_url(REDIS_URL)

#disconnect from redis
async def disconnect_from_redis():
    redis.close()