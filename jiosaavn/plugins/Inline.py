from pyrogram import Client, filters
from pyrogram.types import InlineQueryResultArticle, InlineQueryResultPhoto, InlineKeyboardMarkup, InlineKeyboardButton, InputTextMessageContent, ChosenInlineResult, InputMediaAudio    
from ..tools.request import req


@Client.on_inline_query()
async def search_inline(c, m):
    if m.query == '':
        await m.answer(
            results=[],
            cache_time=0,
            switch_pm_text=f"🔎 Type the song name for searching...",
            switch_pm_parameter="help",
        )
        return

    offset = m.offset if m.offset else 1
    url = 'https://www.jiosaavn.com/api.php?'
    params = {
        'p': offset,
        'q': m.query.replace('Album:', '').strip(),
        '_format': 'json',
        '_marker': 0,
        'api_version': 4,
        'ctx': 'wap6dot0',
        'n': 5
    }

    if 'Album:' in m.query:
        params['__call'] = 'search.getAlbumResults'
        data = await req(url, params)
        if 'total' in data:
            if data['total'] == 0:
                await m.answer(
                    results=[],
                    cache_time=0,
                    switch_pm_text=f"❌ No Album search result found for '{m.query.replace('Album:', '').strip()}'",
                    switch_pm_parameter="help",
                )
                return
            print(data)
            for result in data['results']:
                title = result['title'] if 'title' in result else ''
                id = result['id'] if 'id' in result else None
                language = result['language'] if 'language' in result else ''
                

        else:
            await m.answer(
                results=[],
                cache_time=0,
                switch_pm_text=f"🔎 Type the Album name for searching...",
                switch_pm_parameter="help",
            )
            return
