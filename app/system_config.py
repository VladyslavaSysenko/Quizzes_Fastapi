import os
from dotenv.main import load_dotenv
load_dotenv()

app_host = os.environ["APP_HOST"]
app_port = int(os.environ["APP_PORT"])

class DB:
    POSTGRES_USERNAME = os.environ["POSTGRES_USERNAME"]
    POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
    POSTGRES_DB = os.environ["POSTGRES_DB"]
    POSTGRES_HOST = os.environ["POSTGRES_HOST"]
    POSTGRES_PORT = os.environ["POSTGRES_PORT"]
    POSTGRES_URL = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    REDIS_HOST = os.environ["REDIS_HOST"]
    REDIS_PORT = os.environ["REDIS_PORT"]
    REDIS_URL = os.environ["REDIS_URL"]