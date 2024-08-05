import html
import logging
import traceback

from api.jiosaavn import Jiosaavn
from jiosaavn.bot import Bot

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

logger = logging.getLogger(__name__)

@Client.on_callback_query(filters.regex(r"^artist#"))
async def artist(client: Bot, callback: CallbackQuery):
    await callback.answer()
    data = callback.data.split("#")
    artist_id = data[1]
    page_no = int(data[2]) if len(data) == 3 else 1
    msg = callback.message

    try:
        response = await Jiosaavn().get_artist(artist_id=artist_id, page_no=page_no)
        if not response or not response.get("topSongs"):
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="search#artists")]])
            return await callback.message.edit(
                "**Currently, only songs by this artist are displayed.\n\n"
                "No additional songs are available at the moment**",
                reply_markup=reply_markup
            )
    except RuntimeError as e:
        logger.error(e)
        traceback.print_exc()
        return await msg.edit("Connection refused by JioSaavn API. Please try again.")

    name = response.get("name")
    songs = response.get("topSongs")
    total_results = response.get("count", 0)
    image_url = response.get("image")
    image_url = image_url.replace("150x150", "500x500") if image_url else None
    artist_url = response.get("urls", {}).get("songs")
    follower_count = int(response.get("follower_count", "0"))
    dob = response.get("dob")

    buttons = []
    for song in songs:
        try:
            song_title = song.get("title", "")
            song_title = html.unescape(song_title)
            button_label = f"🎙 {song_title}"
            song_id = song.get("perma_url", "").rsplit("/", 1)[1]
            if song_id:
                callback_data = f"song#{song_id}#{artist_id}#artist"
                buttons.append([InlineKeyboardButton(button_label, callback_data=callback_data)])
        except IndexError:
            pass

    navigation_buttons = []
    if page_no > 1:
        navigation_buttons.append(InlineKeyboardButton("⬅️ Previous", callback_data=f"artist#{artist_id}#{page_no-1}"))
    if total_results > 10 * page_no:
        navigation_buttons.append(InlineKeyboardButton("➡️ Next", callback_data=f"artist#{artist_id}#{page_no+1}"))
    if navigation_buttons:
        buttons.append(navigation_buttons)

    buttons.append([InlineKeyboardButton("🔙 Back", callback_data="search#artists")])

    text_data = (
        f"[\u2063]({image_url})"
        f"**👨‍🎤 Artist:** [{name}]({artist_url})" if name else '',
        f"**📜 Page No:** {page_no}",
        f"**🔊 Total Songs:** {total_results}" if total_results else "",
        f"**👥 Followers:** {follower_count:,}" if follower_count else "",
        f"**📆 Date of Birth:** __{dob}__" if dob else '',
    )
    text = "\n\n".join(filter(None, text_data))

    await msg.edit(text, reply_markup=InlineKeyboardMarkup(buttons))
