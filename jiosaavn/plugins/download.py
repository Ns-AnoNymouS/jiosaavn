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
    else:
        send_msg = m.message
        cmd, id, type = m.data.split('+')

    if type == 'song':
        await download_tool(c, id)


async def download_tool(c, id):
    is_exist = await c.db.is_id_exist(id)
