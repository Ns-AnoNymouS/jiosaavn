from os import getenv

API_ID = 24620300
API_HASH = "9a098f01aa56c836f2e34aee4b7ef963"
BOT_TOKEN = "7002313119:AAGXwPqwcPmEkRhqmh6xUBw_3NDjme5bMVI"
BOT_COMMANDS = (
    ("start", "Initialize the bot and check its status"),
    ("settings", "Configure and manage bot settings"),
    ("help", "Get information on how to use the bot"),
    ("about", "Learn more about the bot and its features"),
)

DATABASE_URL = "mongodb+srv://botmaker9675208:botmaker9675208@cluster0.sc9mq8b.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
HOST = getenv("HOST", "0.0.0.0")
PORT = int(getenv("PORT", "8080"))
