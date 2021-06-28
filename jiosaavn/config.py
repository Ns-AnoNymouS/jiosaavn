import os

class Config(object):
    API_HASH = os.environ.get("API_HASH")
    API_ID = int(os.environ.get("API_ID", 12345))
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    DATABASE_URL = os.environ.get("DATABASE_URL", "")
