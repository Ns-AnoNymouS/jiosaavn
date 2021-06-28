from pyrogram import Client, filters


@Client.on_callback_query(filters.regex('^open$'))
async def opensong(c, m):
    await m.edit()
