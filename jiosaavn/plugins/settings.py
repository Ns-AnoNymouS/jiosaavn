from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..tools.request import req


@Client.on_message(filters.command('settings'))
async def settings(c, m, cb=False):
    if not await c.db.is_user_exist(m.from_user.id):
        await c.db.add_user(m.from_user.id)
    type = (await c.db.get_user(m.from_user.id))['type']
    quality = (await c.db.get_user(m.from_user.id))['quality']
    tx1 = '✅ All' if type == 'all' else 'All'
    tx2 = '✅ Albums' if type == 'album' else 'Albums' 
    tx3 = '✅ Songs' if type == 'song' else 'Songs'
    buttons = [[
        InlineKeyboardButton(tx1, callback_data='settings+type+all'),
        InlineKeyboardButton(tx2, callback_data='settings+type+album'),
        InlineKeyboardButton(tx3, callback_data='settings+type+song'),
        ],[
        InlineKeyboardButton(),
        InlineKeyboardButton()
    ]]
    text = '**Select the search result type and music quality 🧏‍♂️**'
    if cb:
        try:
            await m.message.edit(text, reply_markup=InlineKeyboardMarkup(buttons))
        except:
            pass
    else:
        await m.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), quote=True)


@Client.on_callback_query(filters.regex('^settings\+'))
async def settings_cb(c, m):
    cmd, key, value = m.data.split('+')
    await c.db.update_user(m.from_user.id, key, value)
    await m.answer()
    await settings(c, m, True)
