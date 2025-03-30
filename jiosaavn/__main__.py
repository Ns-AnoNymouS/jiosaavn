import logging
import logging.config
import importlib

try:
    import uvloop
    uvloop.install()
except ImportError:
    pass

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
