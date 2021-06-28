from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..tools.request import req

@Client.on_callback_query(filters.command('settings'))
async def settings(c, m):
