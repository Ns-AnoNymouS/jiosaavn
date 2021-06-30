from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_message(filters.command('start') & filters.private & filters.incoming)
async def start(c, m):
    text = f"Hi {m.from_user.mention(style='md')},\n\nI am a telegram prowerful jiosaavn bot helps you to search and download songs, playlists, Albums, etc from jiosaavn.\n\n**Maintained By:** [Anonymous](https://t.me/Ns_AnoNymous)"
    buttons = [[
        InlineKeyboardButton('My Father 🧑', url='https://t.me/Ns_AnoNymous'),
        InlineKeyboardButton('About 📕', callback_data='about')
        ],[
        InlineKeyboardButton('Help 💡', callback_data='help'),
        InlineKeyboardButton('Settings ⚙', callback_data='settings')
        ],[
        InlineKeyboardButton
    ]]
    await m.reply_text(text)
