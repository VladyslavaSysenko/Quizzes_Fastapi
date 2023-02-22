import os
from dotenv.main import load_dotenv
load_dotenv()

app_host = os.environ["APP_HOST"]
app_port = int(os.environ["APP_PORT"])