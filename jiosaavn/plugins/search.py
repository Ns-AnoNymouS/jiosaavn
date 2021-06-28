from pyrogram import Client, filters
from ..tools.request import req


@Client.on_message(filters.text & filters.incoming & filters.private & ~filters.regex('.*http.*'))
async def search(c, m):
    send_msg = await m.reply_text('**Processing... ⏳**', quote=True)

    api_url = 'https://www.jiosaavn.com/api.php?'
    params = {
        'p': 1,
        'q': m.text,
        '_format': 'json',
        '_marker': 0,
        'api_version': 4,
        'ctx': 'wap6dot0',
        'n': 10,
        '__call': 'search.getResults'
    }
    data = await req(api_url, params)

    total_results = data['total']
    buttons = []
    for result in data['results']:
        buttons.append([InlineKeyboardButton('', callback_data='')])
    print(data)
