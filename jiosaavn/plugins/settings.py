from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..tools.request import req


@Client.on_message(filters.command('settings'))
async def settings(c, m, cb=False):
    if not await c.db.is_user_exist(m.from_user.id):
        await c.db.add_user(m.from_user.id)
    type = await c.db.get_type(m.from_user.id)
    tx1 = '✅ All' if type == 'all' else 'All'
    tx2 = '✅ Albums' if type == 'album' else 'Albums' 
    tx3 = '✅ Songs' if type == 'song' else 'Songs'
    buttons = [[
        InlineKeyboardButton(tx1, callback_data='settings+all'),
        InlineKeyboardButton(tx2, callback_data='settings+album'),
        InlineKeyboardButton(tx3, callback_data='settings+song')
    ]]
    text = '**Select the search result type 🧏‍♂️**'
    if cb:
        try:
            await m.message.edit(text, reply_markup=InlineKeyboardMarkup(buttons))
        except:
            pass
    else:
        await m.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), quote=True)


@Client.on_callback_query(filters.regex('^settings\+'))
async def settings_cb(c, m):
    cmd, status = m.data.split('+')
