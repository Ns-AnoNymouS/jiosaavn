from pyrogram import Client, filters


@Client.on_callback_query(filters.regex('^open$'))
async def opensong(c, m):
    url = 'https://www.jiosaavn.com/api.php?'
    params = {
        '__call': 'song.getDetails',
        'cc': 'in',
        '_marker': '0%3F_marker%3D0',
        '_format': 'json',
        'pids': 
    }
    await m.edit()
