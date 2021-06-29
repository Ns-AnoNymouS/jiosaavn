from pyrogram import Client, filters
from pyrogram.types import InlineQueryResultArticle, InlineQueryResultPhoto, InlineKeyboardMarkup, InlineKeyboardButton, InputTextMessageContent    
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

    offset = int(m.offset) if m.offset else 1
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

            inlineresults = []
            for result in data['results']:
                title = result['title'] if 'title' in result else ''
                id = result['id'] if 'id' in result else None
                language = result['language'] if 'language' in result else ''
                album_url = result['perma_url'].encode().decode() if 'perma_url' in result else ''
                year = result['year'] if 'year' in result else ''
                songs = result['more_info']['song_count'] if 'more_info' in result else 0
                description = result['subtitle'] if 'subtitle' in result else ''
                image_url = result['image'].replace('150x150', '500x500').encode().decode() if 'image' in result else None
                inlinedescription = f"• Total Songs: {songs}\n• Language: {language}\n• Year: {year}"

                text = f"[\u2063]({image_url})"
                text += f"**📚 Album:** [{title}]({album_url})\n\n" if 'title' in result else ''
                text += f"**🔊 Total Songs:** {songs}\n\n"
                text += f"**📰 Language:** {language}\n\n"
                text += f"**📆 Year:** __{year}__\n\n"
                text += f"**📋 Description:** {description}"

                button = [[InlineKeyboardButton('Show Songs 👀', callback_data=f'album+{id}')]]
                inlineresults.append(
                    InlineQueryResultArticle(
                        thumb_url=image_url,
                        title=title,
                        description=inlinedescription,
                        input_message_content=InputTextMessageContent(message_text=text),
                        reply_markup=InlineKeyboardMarkup(button)
                ))
            await m.answer(
                results=inlineresults,
                cache_time=0,
                switch_pm_text=f"📚 {data['total']} results found for Album '{m.query.replace('Album:', '').strip()}'",
                switch_pm_parameter="help",
                next_offset=str(offset+1)
            )

        else:
            await m.answer(
                results=[],
                cache_time=0,
                switch_pm_text=f"🔎 Type the Album name for searching...",
                switch_pm_parameter="help",
            )
            return
    else:
        params['__call'] = 'search.getResults'
        data = await req(url, params)
        if 'total' in data:
            if data['total'] == 0:
                await m.answer(
                    results=[],
                    cache_time=0,
                    switch_pm_text=f"❌ No song search result found for '{m.query}'",
                    switch_pm_parameter="help",
                )
                return

            inlineresults = []
            for result in data['results']:
                title = result['title'] if 'title' in result else ''
                id = result['id'] if 'id' in result else None
                language = result['language'] if 'language' in result else ''
                song_url = result['perma_url'].encode().decode() if 'perma_url' in result else ''
                play_count = result['play_count'] if 'play_count' in result else 0
                album = result['more_info']['album'] if 'album' in result['more_info'] else ''
                album_url = result['more_info']['album_url'] if 'album_url' in result['more_info'] else ''
                year = result['year'] if 'year' in result else ''
                description = result['subtitle'] if 'subtitle' in result else ''
                image_url = result['image'].replace('150x150', '500x500').encode().decode() if 'image' in result else None
                music = result['music'] if 'music' in result else ''
                inlinedescription = f"• Album: {album}\n• Plays Count: {play_count}\n• Music: {music}\n• Language: {language}\n• Year: {year}"

                text = f"[\u2063]({image_url})"
                text += f"**🎙 Song:** [{title}]({song_url})\n\n"
                text += f"**📚 Album:** [{album}]({album_url})\n\n" if 'title' in result else ''
                text += f"**▶️ Plays Count:** {play_count}\n\n"
                text += f"**🥁 Music:** {music}\n\n"
                text += f"**📰 Language:** {language}\n\n"
                text += f"**📆 Year:** __{year}__\n\n"
                text += f"**📋 Description:** {description}"

                button = [[
                    InlineKeyboardButton('Lyrics 🧾', callback_data='lyrics'),
                    InlineKeyboardButton('Upload to TG 📤', callback_data=f'upload+{id}+song')
                    ],[
                    InlineKeyboardButton('Search Song 🔍', switch_inline_query=""),
                    InlineKeyboardButton('Search Album 🔍', switch_inline_query="Album: ")
                ]]

                inlineresults.append(
                    InlineQueryResultArticle(
                        thumb_url=image_url,
                        title=title,
                        description=inlinedescription,
                        input_message_content=InputTextMessageContent(message_text=text),
                        reply_markup=InlineKeyboardMarkup(button)
                ))
            await m.answer(
                results=inlineresults,
                cache_time=0,
                switch_pm_text=f"📚 {data['total']} results found for song '{m.query.replace('Album:', '').strip()}'",
                switch_pm_parameter="help",
                next_offset=str(offset+1)
            )

        else:
            await m.answer(
                results=[],
                cache_time=0,
                switch_pm_text=f"🔎 Type the song name for searching...",
                switch_pm_parameter="help",
            )
            return
