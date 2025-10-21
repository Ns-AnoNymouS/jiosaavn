import html
import logging
import traceback

from api.jiosaavn import Jiosaavn
from jiosaavn.bot import Bot

from pyrogram import filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import MessageNotModified

logger = logging.getLogger(__name__)

@Bot.on_callback_query(filters.regex(r"^search#"))
@Bot.on_message(
    filters.text & filters.incoming & filters.private & 
    ~filters.regex(r'^http.*') & ~filters.via_bot & 
    ~filters.command(["start", "settings", "help", "about"])
)
async def search(client: Bot, message: Message|CallbackQuery):
    if isinstance(message, Message):
        send_msg = await message.reply("__**Processing... ⏳**__", quote=True)
    else:
        await message.answer()
        send_msg = message.message

    query = message.text if isinstance(message, Message) else message.message.reply_to_message.text
    page_no = 1
    if isinstance(message, Message):
        user_data = await client.db.get_user(message.from_user.id)
        search_type = user_data['type']
    else:
        data = message.data.split('#')
        search_type = data[1]
        if len(data) == 3:
            page_no = int(data[2])

    try:
        if search_type in ('all', 'topquery'):
            response = await Jiosaavn().search_all_types(query=query)
        else:
            response = await Jiosaavn().search(query=query, search_type=search_type, page_no=page_no)
    except RuntimeError as e:
        logger.error(e)
        traceback.print_exc()
        return await send_msg.edit("Connection refused by jiosaavn api. Please try again")

    if not response:
        return await send_msg.edit(f'🔎 No search result found for your query `{query}`')

    buttons = []
    if search_type == "all" or search_type == "topquery":
        button_song_type_map = {
            "songs": (f"🎙 Songs", f"search#songs"),
            "albums": (f"📚 Albums", f"search#albums"),
            "playlists": (f"💾 Playlists", f"search#playlists"),
            "artists": (f"👨‍🎤 Artists", f"search#artists"),
            "topquery": (f"✨ Top Result", f"search#topquery"),
        }

        if search_type == 'topquery':
            sub_sorted_data = sorted(
                response.get("topquery", {}).get("data", []),
                key=lambda x: x.get("position", 0)
            )
            for data in sub_sorted_data:
                title = data.get("title", "unkown")
                title = html.unescape(title)
                album = data.get("album")
                item_type = data.get("type")
                item_id = data.get("url", "/").rsplit("/", 1)[1]
                type_emoji_map = {
                    "song": "🎙",
                    "album": "📚",
                    "playlist": "💾",
                    "artist": "👨‍🎤",
                }
                if item_type not in type_emoji_map:
                    continue
                emoji = type_emoji_map[item_type]
                button_text = f"{emoji} {title} from {album}" if album else f"{emoji} {title}"
                callback_data = f"{item_type}#{item_id}#topquery" if item_type == "song" else f"{item_type}#{item_id}#topquery"
                buttons.append([InlineKeyboardButton(text=button_text, callback_data=callback_data)])
        else:
            sorted_data = sorted(response.items(), key=lambda value: value[1].get("position", 0))
            for result_type, result in sorted_data:
                if result_type not in button_song_type_map:
                    continue

                if result.get("data"):
                    button_label, callback_data = button_song_type_map.get(result_type, (None, None))
                    buttons.append([InlineKeyboardButton(text=button_label, callback_data=callback_data)])
        text = f"**🔍 Search Query:** {query}\n\n__Please select one catogery 👇__"
    else:
        total_results = response.get("total", 0)

        for result in response.get("results", []):
            item_id = result.get("perma_url", "/").rsplit("/", 1)[1]
            title = result.get("title", "unknown")
            title = html.unescape(title)
            result_type = result.get("type", "unknown")
            artist = result.get("name", "unknown")
            artist = html.unescape(artist)
            more_info = result.get("more_info", {})
            album = more_info.get("album", "")

            button_label_map = {
                "song": f"🎙 {title} from '{album}'" if album else f"🎙 {title}",
                "album": f"📚 {title}",
                "playlist": f"💾 {title}",
                "artist": f"👨‍🎤 {artist}",
            }

            button_label = button_label_map.get(result_type)
            if button_label:
                buttons.append([InlineKeyboardButton(text=button_label, callback_data=f"{result_type}#{item_id}")])

        text = f"**📈 Total Results:** {total_results}\n\n**🔍 Search Query:** {query}\n\n**📜 Page No:** {page_no}"
        navigation_buttons = []
        if page_no > 1:
            navigation_buttons.append(InlineKeyboardButton("⬅️", callback_data=f"search#{search_type}#{page_no-1}"))
        if total_results > 10 * page_no:
            navigation_buttons.append(InlineKeyboardButton("➡️", callback_data=f"search#{search_type}#{page_no+1}"))
        if navigation_buttons:
            buttons.append(navigation_buttons)

    if not buttons:
        return await send_msg.edit(f'🔎 No search result found for your query `{query}`')

    buttons.append([InlineKeyboardButton('Close ❌', callback_data="close")])
    try:
        if send_msg.text != text or send_msg.reply_markup != InlineKeyboardMarkup(buttons):
            await send_msg.edit(text, reply_markup=InlineKeyboardMarkup(buttons))
    except MessageNotModified:
        logger.warning("Message not modified in search_handler")
    except Exception as e:
        logger.error(f"Failed to edit message in search_handler: {e}")
        await send_msg.edit("An error occurred while updating search results.")
