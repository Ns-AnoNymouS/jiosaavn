import os
import html
import time
import shutil
import logging

from jiosaavn.bot import Bot
from api.jiosaavn import Jiosaavn

import aiohttp
import aiofiles
from pyrogram import filters
from pyrogram.types import Message, CallbackQuery
from pyrogram.enums import ChatAction

logger = logging.getLogger(__name__)

@Bot.on_callback_query(filters.regex(r"^upload#"))
@Bot.on_message(filters.regex(r"http.*") & filters.private & filters.incoming)
async def download(client: Bot, message: Message|CallbackQuery):
    if isinstance(message, CallbackQuery):
        _, item_id, search_type = message.data.split("#")
        msg = await message.message.edit("**Processing...**")
    else:
        msg = await message.reply("**Processing...**", quote=True)
        msg.reply_to_message = message
        query = message.text
        item_id = query.rsplit("/", 1)[1]
        if "song" in query:
            search_type = "song"
        elif "album" in query:
            search_type = "album"
        elif "featured" in query:
            search_type = "playlist"
        elif "artist" in query:
            search_type = "artist"

    if search_type == "song":
        await download_tool(client, message, msg, item_id)
    elif search_type in ("album", "playlist"):
        page_no = 1
        album_id = item_id if search_type == "album" else None
        playlist_id = item_id if search_type == "playlist" else None

        while True:
            response = await Jiosaavn().get_playlist_or_album(
                album_id=album_id, 
                playlist_id=playlist_id, 
                page_no=page_no
            )
            
            if not response or not response.get("list"):
                break
            
            songs = response["list"]
            for song in songs:
                song_url = song.get("perma_url", "")
                if not song_url:
                    continue
                song_id = song_url.rsplit("/", 1)[-1]
                await download_tool(client, message, msg, song_id)
            page_no += 1
    else:
        await msg.edit("Artists and Podcast upload not supported.")
        return

    if "Failed" not in msg.text:
        await msg.delete()

async def download_tool(client: Bot, message: Message|CallbackQuery, msg: Message, song_id: str):
    is_exist = await client.db.is_song_id_exist(song_id)
    user = await client.db.get_user(message.from_user.id)
    quality = user['quality']
    bitrate = 320 if quality == "320kbps" else 160

    if is_exist:
        song = (await client.db.get_song(song_id)).get(quality)
        if song:
            song_msg = await client.get_messages(chat_id=int(song.get('chat_id')), message_ids=int(song.get('message_id')))
            if not song_msg.empty:
                is_sent = await song_msg.copy(message.from_user.id, reply_to_message_id=msg.reply_to_message.id)
                if is_sent:
                    return

    # Extract song data
    song_response = await Jiosaavn().get_song(song_id=song_id)
    song_data = song_response["songs"][0]

    # Extract metadata
    title = song_data.get("title", "Unknown")
    title = html.unescape(title)
    formatted_title = title.replace(" ", "-")
    language = song_data.get("language", "Unknown")
    more_info = song_data.get("more_info", {})
    album = more_info.get("album", "Unknown")
    artist_map = more_info.get("artistMap", {})
    artists = artist_map.get("artists", [])

    def get_artist_by_role(role: str) -> str:
        return ", ".join(artist.get("name") for artist in artists if artist.get("role") == role)

    singers = get_artist_by_role("singer")
    release_date = more_info.get("release_date")
    duration = int(more_info.get("duration", "0"))
    release_year = song_data.get("year")
    album_url = more_info.get("album_url", "")
    image_url = song_data.get("image", "").replace("150x150", "500x500")
    song_url = song_data.get('perma_url', f"https://jiosaavn.com/songs/{formatted_title}/{song_id}")

    # Create caption
    text_data = [
        f"[\u2063]({image_url})"
        f"**🎧 Song:** [{title}]({song_url})" if title else '',
        f"**📚 Album:** [{album}]({album_url})" if album else '',
        f"**📰 Language:** {language}" if language else '',
        f"**📆 Release Date:** __{release_date}__" if release_date else '',
        f"**📆 Release Year:** __{release_year}__" if not release_date and release_year else '',
    ]

    caption = "\n\n".join(filter(None, text_data))

    # Download and upload song
    download_dir = f"./download/{time.time()}{message.from_user.id}/"
    if not os.path.isdir(download_dir):
        os.makedirs(download_dir)

    file_name = f"{download_dir}{title}_{quality}.mp3"
    thumbnail_location = f"{download_dir}{title}.jpg"

    await msg.edit(f"__📥 Downloading {title}__")
    await client.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.RECORD_AUDIO
    )

    async with aiohttp.ClientSession() as session: 
        async with session.get(image_url) as response:
            async with aiofiles.open(thumbnail_location, "wb") as file:
                await file.write(await response.read())

    audio = await Jiosaavn().download_song(song_id=song_id, bitrate=bitrate, download_location=file_name)
    await msg.edit(f"__📤 Uploading {title}__")
    await client.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.UPLOAD_AUDIO
    )

    song_file = await client.send_audio(
        chat_id=message.from_user.id,
        audio=audio,
        caption=caption,
        duration=duration,
        title=title,
        thumb=thumbnail_location,
        performer=singers,
        reply_to_message_id=msg.reply_to_message.id,
        )
    
    if not song_file:
        return await msg.edit(text=f"Failed to upload {song}")

    await client.db.update_song(song_id, quality, song_file.chat.id, song_file.id)
    shutil.rmtree(download_dir)