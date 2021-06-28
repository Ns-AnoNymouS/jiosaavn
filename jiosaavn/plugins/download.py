from pyrogram import Client, filters


@Client.on_message(filters.regex('.*http. *') & filters.private & filters.incoming)
async def download(c, m):
    
