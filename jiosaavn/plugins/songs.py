from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..tools.request import req


@Client.on_callback_query(filters.regex('^open\+'))
async def opensong(c, m):
    await m.answer()
    id = m.data.split('+')
    song_id = m.data.split('+')[1]
    album_id = None
    if len(id) == 3:
        album_id = m.data.split('+')[2]

    url = 'https://www.jiosaavn.com/api.php?'
    params = {
        '__call': 'song.getDetails',
        'cc': 'in',
        '_marker': '0%3F_marker%3D0',
        '_format': 'json',
        'pids': song_id
    }
    data = await req(url, params)
    print(data)
