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

    if m.query == 'Album: '
        await m.answer(
            results=[],
            cache_time=0,
            switch_pm_text=f"🔎 Type the Album name for searching...",
            switch_pm_parameter="help",
        )
        return

    offset = m.offset if m.offset else 0
    
