from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..tools.request import req


@Client.on_message(filters.regex('.*http. *') & filters.private & filters.incoming)
async def download(c, m, cb=False):
    if not cb:
        send_msg = await m.reply_text('Checking...🕵‍♂️', quote=True)
        if 'jiosaavn' not in m.text:
            await send_msg.edit('__Currently only jiosaavn links are supported 🤭__')
        type = 'song' if 'song' in m.text else 'album'
        id = m.text.split('/')[-1]
        reply_to_message_id = m.message_id
    else:
        send_msg = m.message
        cmd, id, type = m.data.split('+')
        reply_to_message_id = m.message.reply_to_message.message_id

    if type == 'song':
        await download_tool(c, id, reply_to_message_id)


async def download_tool(c, id, reply_to_message_id):
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
