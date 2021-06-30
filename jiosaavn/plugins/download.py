import os
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
from ..tools.request import req
from ..tools.upload_helpers import send_audio, copy

@Client.on_message(filters.regex('.*http. *') & filters.private & filters.incoming)
async def download(c, m, cb=False):
    if not cb:
        send_msg = await m.reply_text('**Checking...🕵‍♂️**', quote=True)
        if 'jiosaavn' not in m.text:
            await send_msg.edit('__Currently only jiosaavn links are supported 🤭__')
        type = 'song' if 'song' in m.text else 'album'

        if type == 'song':
            async with aiohttp.ClientSession() as session:
                async with session.get(m.text, data=[('bitrate', '320')]) as response:
                    try:
                        id = (await response.text()).split('"song":{"type":"')[1].split('","image":')[0].split('"id":"')[-1]
                    except IndexError:
                        try:
                            id = ((await response.text()).split('"pid":"'))[1].split('","')[0]
                        except:
                            return await send_msg.edit("**Invalid link 🤦**")
                    except:
                        return await send_msg.edit("**Invalid link 🤦**")

        elif type == 'album':
            async with aiohttp.ClientSession() as session:
                async with session.get(m.text) as response:
                    try:
                        id = (await response.text()).split('"album_id":"')[1].split('"')[0]
                    except IndexError:
                        try:
                            id = (await response.text()).split('"page_id","')[1].split('","')[0]
                        except:
                            return await send_msg.edit("**Invalid link 🤦**")
                    except:
                        return await send_msg.edit("**Invalid link 🤦**")

        reply_to_message_id = m.message_id
    else:
        if m.inline_message_id:
            send_msg = await c.send_message(chat_id=m.from_user.id, text="**Processing...**")
            reply_to_message_id = None
        else:
            send_msg = m.message
            await m.message.edit('**Processing...**')
            reply_to_message_id = m.message.reply_to_message.message_id
        cmd, id, type = m.data.split('+')

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
        'albumid': id
    }
    data = await req(url, params)
    album_url = data['perma_url'].encode().decode() if 'perma_url' in data else ''
    image_url = data['image'].encode().decode().replace("150x150", "500x500") if 'image' in data else ''
    text = f"**📚 Album:** [{data['title']}]({album_url})\n\n" if 'title' in data else ''
    text += f"**📆 Release Date:** __{data['release_date']}__\n\n" if 'release_date' in data else ''

    try:
        send_ms = await c.send_photo(chat_id=m.from_user.id, photo=image_url, caption=text, reply_to_message_id=reply_to_message_id)
        await send_msg.delete()
    except:
        pass

    songs = data['songs']
    for song in songs:
        id = song['id'] if 'id' in song else None
        await download_tool(c, m, id, reply_to_message_id, send_ms)
    try:
        await send_ms.edit(text)
    except:
        pass


async def download_tool(c, m, id, reply_to_message_id, msg):
    is_exist = await c.db.is_id_exist(id)
    if not await c.db.is_user_exist(m.from_user.id):
        await c.db.add_user(m.from_user.id)
    quality = (await c.db.get_user(m.from_user.id))['quality']

    if is_exist:
        try:
            song = (await c.db.get_song(id))[quality]
            song_msg = await c.get_messages(chat_id=int(song.get('chat_id')), message_ids=int(song.get('message_id')))
            if not song_msg.empty:
                is_sent = await copy(song_msg, m.from_user.id, reply_to_message_id)
                if is_sent:
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
    if data['320kbps']=="true" and :
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
            chat_id=m.from_user.id,
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
            chat_id=m.from_user.id,
            action="upload_audio"
        )
    except:
        pass

    song_file = await send_audio(c, m.from_user.id, file_name, text, int(duration), song, thumbnail_location, artists, reply_to_message_id)
    if not song_file:
        return await c.send_message(chat_id=m.from_user.id, text=f"Failed to upload {song}")
    try:
        await c.db.update_song(id, quality, song_file.chat.id, song_file.message_id)
        os.remove(file_name)
    except:
        pass
