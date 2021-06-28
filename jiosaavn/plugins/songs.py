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
    data = (await req(url, params))[song_id]
    album_url = data['album_url'].encode().decode() if 'album_url' in data else ''
    image_url = data['image'].encode().decode().replace("150x150", "500x500") if 'image' in data else ''
    song_url = data['perma_url'].encode().decode() if 'perma_url' in data else ''

    text = f"[\u2063]({image_url})"
    text += f"**🎧 Song:** [{data['song']}]({song_url})\n\n" if 'song' in data else ''
    text += f"**📚 Album:** [{data['album']}]({album_url})\n\n" if 'album' in data else ''
    text += f"**🥁 Music:** {data['music']}\n\n" if 'music' in data else ''
    text += f"**👨‍🎤 Singers:** {data['singers']}\n\n" if 'singers' in data else ''
    text += f"**📰 Language:** {data['language']}\n\n" if 'language' in data else ''
    text += f"**📆 Release Date:** __{data['release_date']}__\n\n" if 'release_date' in data else ''

    type = await c.db.get_type(m.from_user.id)
    if type == 'all':
        call = 'autocomplete.get'
    elif type == 'album':
        call = 'search.getAlbumResults'
    elif type == 'song':
        call = 'search.getResults'

    buttons = [[
        InlineKeyboardButton('lyrics', callback_data='lyrics'),
        InlineKeyboardButton('upload to tg', callback_data='up')
        ],[
        InlineKeyboardButton('Back', callback_data=f'nxt+{call}+1')
    ]]
    await m.message.edit(text, reply_markup=InlineKeyboardMarkup(buttons))
    
    print(data)
