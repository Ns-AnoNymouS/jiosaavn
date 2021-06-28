from pyrogram import Client, filters
from ..tools.request import req

@Client.on_message(filters.text & filters.incoming & filters.private)
async def search(c, m):
