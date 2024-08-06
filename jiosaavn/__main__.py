import logging
import logging.config

import uvloop
uvloop.install()

import importlib
from dotenv import load_dotenv


def main():
    # Get logging configurations
    logging.config.fileConfig('logging.conf')
    logging.getLogger().setLevel(logging.INFO)
    logging.getLogger("pyrogram").setLevel(logging.WARNING)

    load_dotenv()
    bot = importlib.import_module("jiosaavn.bot").Bot
    bot().run()


if __name__ == "__main__" :
    main()
