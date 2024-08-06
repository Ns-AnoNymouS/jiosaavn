from .database import Database
from .config.settings import API_ID, API_HASH, BOT_TOKEN, DATABASE_URL, BOT_COMMANDS
from .app_webpage import start_web, stop_web

from pyrogram import Client
from pyrogram.types import BotCommand, BotCommandScopeAllPrivateChats


class Bot(Client):

    def __init__(self):
        super().__init__( 
            name="jiosaavn",
            bot_token=BOT_TOKEN,
            api_id=API_ID,
            api_hash=API_HASH,
            sleep_threshold=30,
            max_concurrent_transmissions=10,
            plugins={
                "root": "jiosaavn/plugins"
            }
        )
        self.db = Database(DATABASE_URL)

    async def start(self):
        await super().start()
        self.web_runner = await start_web()
        print(f"New session started for {self.me.first_name}({self.me.username})")
        await self.add_commands()

    async def stop(self):
        await super().stop()
        await stop_web(self.web_runner)
        print("Session stopped. Bye!!")

    async def add_commands(self):
        commands = [
            BotCommand(command.strip(), description.strip()) for command, description in BOT_COMMANDS
        ]
        await self.set_bot_commands(
            commands=commands,
            scope=BotCommandScopeAllPrivateChats()
        )