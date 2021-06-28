from pyrogram import Client, filters
from ..tools.request import req


api_url = 'https://www.jiosaavn.com/api.php?'
@Client.on_message(filters.text & filters.incoming & filters.private & ~)
async def search(c, m):
    send_msg = await m.reply_text('**Processing... ⏳**', quote=True)

    
    data = await req()
