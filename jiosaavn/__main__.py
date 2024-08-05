import logging
import logging.config
import uvloop
uvloop.install()
# Get logging configurations
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger().setLevel(logging.WARNING)
logging.getLogger().setLevel(logging.INFO)
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from .bot import Bot
from dotenv import load_dotenv


def main():
    load_dotenv()
    Bot().run()


if __name__ == "__main__" :
    main()
