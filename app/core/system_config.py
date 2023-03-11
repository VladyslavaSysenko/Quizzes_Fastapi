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

class DB_TEST:
    TEST_USERNAME = os.environ["TEST_USERNAME"]
    TEST_PASSWORD = os.environ["TEST_PASSWORD"]
    TEST_DB = os.environ["TEST_DB"]
    TEST_HOST = os.environ["TEST_HOST"]
    TEST_PORT = os.environ["TEST_PORT"]
    db_url_test = f"postgresql+asyncpg://{TEST_USERNAME}:{TEST_PASSWORD}@{TEST_HOST}:{DB.POSTGRES_PORT}/{TEST_DB}"

class AUTH0:
    DOMAIN = os.environ["DOMAIN"]
    API_AUDIENCE = os.environ["API_AUDIENCE"]
    ALGORITHMS = os.environ["ALGORITHMS"]
    ISSUER = os.environ["ISSUER"]
    SECRET_KEY = os.environ["SECRET_KEY"]
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])