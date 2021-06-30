from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..tools.request import req


@Client.on_message(filters.command('settings'))
async def settings(c, m, cb=False):
    if not await c.db.is_user_exist(m.from_user.id):
        await c.db.add_user(m.from_user.id)
    user = await c.db.get_user(m.from_user.id)
    type = user['type']
    quality = user['quality']
    tx1 = '✅ All' if type == 'all' else 'All'
    tx2 = '✅ Albums' if type == 'album' else 'Albums' 
    tx3 = '✅ Songs' if type == 'song' else 'Songs'
    tx4 = '✅ Artists' if type == 'artists' else 'artists' 
    tx5 = '✅ Playlist' if type == 'playlist' else 'Playlist'
    ql1 = '✅ 320kbps' if quality == '320kbps' else '320kbps'
    ql2 = '✅ 160kbps' if quality == '160kbps' else '160kbps'
    buttons = [[
        InlineKeyboardButton(tx1, callback_data='settings+type+all'),
        InlineKeyboardButton(tx2, callback_data='settings+type+album'),
        InlineKeyboardButton(tx3, callback_data='settings+type+song'),
        ],[
        InlineKeyboardButton(tx4, callback_data='settings+type+artists'),
        InlineKeyboardButton(tx5, callback_data='settings+type+playlist'),
        ],[
        InlineKeyboardButton(ql1, callback_data='settings+quality+320kbps'),
        InlineKeyboardButton(ql2, callback_data='settings+quality+160kbps')
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
