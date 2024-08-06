import logging
import logging.config

import uvloop
uvloop.install()

from .bot import Bot
from dotenv import load_dotenv


def main():
    # Get logging configurations
    logging.config.fileConfig('logging.conf')
    logging.getLogger().setLevel(logging.INFO)
    logging.getLogger("pyrogram").setLevel(logging.WARNING)

    load_dotenv()
    
    Bot().run()


if __name__ == "__main__" :
    main()
