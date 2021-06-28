from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..tools.request import req

@Client.on_callback_query(filters.command('settings'))
async def settings(c, m):
    if not await c.db.is_user_exist(m.from_user.id):
        await c.db.add_user(m.from_user.id)

    await m.reply_text('select the search result type', reply_markup=InlineKeyboardMarkup())
