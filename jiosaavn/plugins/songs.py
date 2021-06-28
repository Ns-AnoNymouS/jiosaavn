from pyrogram import Client, filters


@Client.on_callback_query(filters.regex(''))
async def opensong(c, m):
