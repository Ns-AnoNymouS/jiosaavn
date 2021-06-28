import logging
import logging.config

# Get logging configurations
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger().setLevel(logging.WARNING)
logging.getLogger().setLevel(logging.INFO)
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from .config import Config
from .database.database import Database
from pyrogram import Client 


def main():
    jiosaavn = Client(
        session_name="jiosaavn",
        bot_token = Config.BOT_TOKEN,
        api_id = Config.API_ID,
        api_hash = Config.API_HASH,
        plugins = dict(root="jiosaavn/plugins"),
        workers = 100
    )

    jiosaavn.db = Database(Config.DATABASE_URL, 'jiosaavn')
    jiosaavn.run()


if __name__ == "__main__" :
    main()
