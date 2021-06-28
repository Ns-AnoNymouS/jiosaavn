from pyrogram import Client, filters


@Client.on_message(filters.regex('.*http. *') & filters.private & filters.incoming)
async def download(c, m, cb=False):
    if not cb:
        send_msg = await m.reply_text('Checking...🕵‍♂️', quote=True)
    else:
        send_msg = m.message

