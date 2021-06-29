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
        id = song['id'] if 'id' in song else None
        buttons.append([InlineKeyboardButton(btn_txt, callback_data=f'open+{id}+{album_id}')])

    buttons.append([InlineKeyboardButton('Upload Album 📤', callback_data=f'upload+{album_id}+album')])
    type = await c.db.get_type(m.from_user.id)
    type = 'all' if type == 'all' else 'album'
    back_cb = f'nxt+{type}+1'
    buttons.append([InlineKeyboardButton('🔙', callback_data=back_cb)])

    album_url = data['perma_url'].encode().decode() if 'perma_url' in data else ''
    image_url = data['image'].encode().decode().replace("150x150", "500x500") if 'image' in data else ''

    text = f"[\u2063]({image_url})"
    text += f"**📚 Album:** [{data['title']}]({album_url})\n\n" if 'title' in data else ''
    text += f"**🔊 Total Songs:** {len(songs)}"
    text += f"**📆 Release Date:** __{data['release_date']}__\n\n" if 'release_date' in data else ''

    try:
        await m.message.edit(text, reply_markup=InlineKeyboardMarkup(buttons))
    except:
        pass
