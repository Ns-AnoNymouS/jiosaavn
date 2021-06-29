import os
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..tools.request import req


@Client.on_message(filters.regex('.*http. *') & filters.private & filters.incoming)
async def download(c, m, cb=False):
    if not cb:
        send_msg = await m.reply_text('**Checking...🕵‍♂️**', quote=True)
        if 'jiosaavn' not in m.text:
            await send_msg.edit('__Currently only jiosaavn links are supported 🤭__')
        type = 'song' if 'song' in m.text else 'album'

        async with aiohttp.ClientSession() as session:
            async with session.get(m.text, data=[('bitrate', '320')]) as response:
                try:
                    id = (await response.text()).split('"song":{"type":"')[1].split('","image":')[0].split('"id":"')[-1]
                except IndexError:
                    try:
                        id = ((await response.text()).split('"pid":"'))[1].split('","')[0]
                    except:
                        await send_msg.edit("**Invalid link 🤦**")
        reply_to_message_id = m.message_id
    else:
        send_msg = m.message
        await m.message.edit('**Processing...**')
        cmd, id, type = m.data.split('+')
        reply_to_message_id = m.message.reply_to_message.message_id

    if type == 'song':
        await download_tool(c, m, id, reply_to_message_id, send_msg)
        await send_msg.delete()
        return
    
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
    for song in songs:
        id = song['id'] if 'id' in song else None
        await download_tool(c, m, id, reply_to_message_id, send_msg)
    text += f"**📚 Album:** [{data['title']}]({album_url})\n\n" if 'title' in data else ''
    text += f"**📆 Release Date:** __{data['release_date']}__\n\n" if 'release_date' in data else ''
    await send_msg.edit(text)


async def download_tool(c, m, id, reply_to_message_id, msg):
    is_exist = await c.db.is_id_exist(id)
    if is_exist:
        song = await c.db.get_song(id)
        try:
            song_msg = await c.get_messages(chat_id=int(song.chat_id), message_ids=int(song.message_id))
            if not song_msg.empty:
                await song_msg.copy(chat_id=m.chat.id, reply_to_message_id=reply_to_message_id)
                return
        except:
            pass

    url = 'https://www.jiosaavn.com/api.php?'
    params = {
        '__call': 'song.getDetails',
        'cc': 'in',
        '_marker': '0%3F_marker%3D0',
        '_format': 'json',
        'pids': id
    }
    data = (await req(url, params))[id]
    url = data['media_preview_url'].replace("preview", "aac").encode().decode()
    if data['320kbps']=="true":
        url = url.replace("_96_p.mp4", "_320.mp4")
    else:
        url = url.replace("_96_p.mp4", "_160.mp4")
    song = data['song'] if 'song' in data else 'Unknown'
    artists = data['primary_artists'] if 'primary_artists' in data else 'Unknown'
    duration = data['duration'] if 'duration' in data else 0

    album_url = data['album_url'].encode().decode() if 'album_url' in data else ''
    image_url = data['image'].encode().decode().replace("150x150", "500x500") if 'image' in data else ''
    song_url = data['perma_url'].encode().decode() if 'perma_url' in data else ''

    text = f"**🎧 Song:** [{data['song']}]({song_url})\n\n" if 'song' in data else 'Unknown'
    text += f"**📚 Album:** [{data['album']}]({album_url})\n\n" if 'album' in data else ''
    text += f"**🥁 Music:** {data['music']}\n\n" if 'music' in data else ''
    text += f"**👨‍🎤 Singers:** {data['singers']}\n\n" if 'singers' in data else ''
    text += f"**📰 Language:** {data['language']}\n\n" if 'language' in data else ''
    text += f"**📆 Release Date:** __{data['release_date']}__\n\n" if 'release_date' in data else ''

    file_name = f"./DOWNLOADS/"
    if not os.path.isdir(file_name):
        os.makedirs(file_name)
    file_name = f'{file_name}{song}.mp3'
    thumbnail_location = f'{file_name}{song}.jpeg'

    try:
        await msg.edit(f'__📥 Downloading {song}__')
        await c.send_chat_action(
            chat_id=message.chat.id,
            action="record_audio"
        )
    except:
        pass
    async with aiohttp.ClientSession() as session: 
        async with session.get(url) as response:
            with open(file_name, "wb") as file:
                while True:
                    try:
                        chunk = await response.content.read(4 * 1024 * 1024)
                    except:
                        break
                    if not chunk:
                        break
                    file.write(chunk)

    async with aiohttp.ClientSession() as session: 
        async with session.get(image_url) as response:
            with open(thumbnail_location, "wb") as file:
                while True:
                    try:
                        chunk = await response.content.read(4 * 1024 * 1024)
                    except:
                        break
                    if not chunk:
                        break
                    file.write(chunk)

    try:
        await msg.edit(f'__📤 Uploading {song}__')
        await c.send_chat_action(
            chat_id=message.chat.id,
            action="upload_audio"
        )
    except:
        pass

    song = await c.send_audio(
        chat_id=m.from_user.id,
        audio=file_name,
        caption=text,
        duration=int(duration),
        title=song,
        thumb=thumbnail_location,
        performer=artists,
        parse_mode="markdown"
    )
    await c.db.update_song(id, song.chat.id, song.message_id)
    try:
        os.remove(file_name)
    except:
        pass
