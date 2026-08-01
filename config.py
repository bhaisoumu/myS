from os import getenv
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")

API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")

OWNER_ID = int(getenv("OWNER_ID"))

LOG_GROUP_ID = int(getenv("LOG_GROUP_ID"))
