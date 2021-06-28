from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..tools.request import req


@Client.on_callback_query(filters.regex('^album\+'))
async def openalbum(c, m):
    await m.answer()
    album_id = m.data.split('+')[1]

    url = 'https://www.jiosaavn.com/api.php?'
    params = {
        '__call': 'content.getAlbumDetails',
        'cc': 'in',
        '_marker': '0%3F_marker%3D0',
        '_format': 'json',
        'albumid': album_id
    }
    data = await req(url, params)

    songs = data['songs']
    buttons = []
    for song in songs:
        btn_txt = f"🎙 {song['song']}" if 'song' in song else '🎙 '
        id = song['id']
        buttons.append([InlineKeyboardButton(btn_txt, callback_data='')])
    print(data)
