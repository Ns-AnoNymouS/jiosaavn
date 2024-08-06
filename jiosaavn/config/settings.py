from os import getenv

API_ID = getenv("API_ID")
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")
BOT_COMMANDS = (
    ("start", "Initialize the bot and check its status"),
    ("settings", "Configure and manage bot settings"),
    ("help", "Get information on how to use the bot"),
    ("about", "Learn more about the bot and its features"),
)

DATABASE_URL = getenv("DATABASE_URL", None)
HOST = getenv("HOST", "0.0.0.0")
PORT = int(getenv("PORT", "8080"))
