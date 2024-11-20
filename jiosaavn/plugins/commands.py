import logging
from jiosaavn.bot import Bot
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

logger = logging.getLogger(__name__)

#################### COMMAND ##########

@Bot.on_callback_query(filters.regex('^home$'))
@Bot.on_message(filters.command('start') & filters.private & filters.incoming)
async def start_handler(c: Client, m: Message | CallbackQuery):
    msg = await m.reply("**Checking....🔍**", quote=True)
    # Mention user
    last_name = f' {m.from_user.last_name}' if m.from_user.last_name else ''
    mention = f"[{m.from_user.first_name}{last_name}](tg://user?id={m.from_user.id})"
    
    text = (
        f"**Hello {mention},**\n\n<blockquote>ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ᴊɪᴏsᴀᴀᴠɴ ᴛᴇʟᴇɢʀᴀᴍ ʙᴏᴛ! ᴛʜɪs ᴘᴏᴡᴇʀғᴜʟ ʙᴏᴛ ᴀʟʟᴏᴡs ʏᴏᴜ ᴛᴏ sᴇᴀʀᴄʜ ᴀɴᴅ ᴅᴏᴡɴʟᴏᴀᴅ sᴏɴɢs, ᴘʟᴀʏʟɪsᴛs, ᴀʟʙᴜᴍs, ᴀɴᴅ ᴀʀᴛɪsᴛs ᴅɪʀᴇᴄᴛʟʏ ғʀᴏᴍ ᴊɪᴏsᴀᴀᴠɴ.</blockquote>\n\n"
        "**With this Bot, you can:**\n\n"
        "__- Search for songs, albums, playlists, and artists__\n"
        "__- Download your favorite tracks directly to Telegram__\n"
        "__- Explore various features tailored to enhance your music experience__\n\n"
        "**Maintained By:** [Anonymous](https://t.me/Ns_AnoNymous)"
    )

    buttons = [[
        InlineKeyboardButton('Owner 🧑', url='https://t.me/Ns_AnoNymous'),
        InlineKeyboardButton('About 📕', callback_data='about')
    ], [
        InlineKeyboardButton('Help 💡', callback_data='help'),
        InlineKeyboardButton('Settings ⚙', callback_data='settings')
    ], [
        InlineKeyboardButton('Open Source Repository 🌐', url='https://github.com/Ns-AnoNymouS/jiosaavn')
    ]]
    
    if isinstance(m, Message):
        await msg.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), quote=True)
    else:
        await msg.edit(text, reply_markup=InlineKeyboardMarkup(buttons))

@Bot.on_callback_query(filters.regex('^help$'))
@Bot.on_message(filters.command('help') & filters.private & filters.incoming)
async def help_handler(client: Bot, message: Message | CallbackQuery):
    text = (
        "**It's very simple to use me! 😉**\n\n"
        "1. Start by configuring your preferences using the `/settings` command.\n"
        "2. Send me the name of a song, playlist, album, or artist you want to search for.\n"
        "3. I'll handle the rest and provide you with the results!\n\n"
        "Feel free to explore and enjoy the music!"
    )

    buttons = [[
        InlineKeyboardButton('About 📕', callback_data='about'),
        InlineKeyboardButton('Settings ⚙', callback_data='settings')
        ],[
        InlineKeyboardButton('Home 🏕', callback_data='home'),
        InlineKeyboardButton('Close ❌', callback_data='close')
    ]]

    if isinstance(message, Message):
        await message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), quote=True)
    else:
        await message.message.edit(text, reply_markup=InlineKeyboardMarkup(buttons))

@Bot.on_callback_query(filters.regex('^about$'))
@Bot.on_message(filters.command('about') & filters.private & filters.incoming)
async def about(client: Bot, message: Message|CallbackQuery):
    me = await client.get_me()

    text = (
        f"**🤖 Bot Name:** {me.mention()}\n\n"
        "**📝 Language:** [Python 3](https://www.python.org/)\n\n"
        "**🧰 Framework:** [Pyrogram](https://github.com/pyrogram/pyrogram)\n\n"
        "**👨‍💻 Developer:** [Anonymous](https://t.me/Ns_AnoNymouS)\n\n"
        "**📢 Updates Channel:** [NS Bots](https://t.me/NsBotsOfficial)\n\n"
        "**👥 Support Group:** [AMC Support](https://t.me/amcDevSupport)\n\n"
        "**🔗 Source Code:** [GitHub Repository](https://github.com/Ns-AnoNymouS/jiosaavn)\n\n"
    )

    buttons = [[
        InlineKeyboardButton('Help 💡', callback_data='help'),
        InlineKeyboardButton('Settings ⚙', callback_data='settings')
        ],[
        InlineKeyboardButton('Home 🏕', callback_data='home'),
        InlineKeyboardButton('Close ❌', callback_data='close')
    ]]
    if isinstance(message, Message):
        await message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True, quote=True)
    else:
        await message.message.edit(text, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

@Bot.on_callback_query(filters.regex('^close$'))
async def close_cb(client: Bot, callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await callback.message.reply_to_message.delete()
