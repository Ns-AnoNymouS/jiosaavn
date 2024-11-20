import logging
from jiosaavn.bot import Bot
from jiosaavn.plugins.text import TEXT
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

logger = logging.getLogger(__name__)

#################### COMMAND ##########
@Bot.on_callback_query(filters.regex('^home$'))
@Bot.on_message(filters.command('start') & filters.private & filters.incoming)
async def start(c, m):
    last_name = f' {m.from_user.last_name}' if m.from_user.last_name else ''
    mention = f"[{m.from_user.first_name}{last_name}](tg://user?id={m.from_user.id})" if m.from_user.first_name else f"[User](tg://user?id={m.from_user.id})"
 
    msg = m.message if getattr(m, "data", None) else await m.reply("**Processing....⌛**", quote=True)
    try:
        buttons = [[
            InlineKeyboardButton('Owner 🧑', url='https://t.me/Ns_AnoNymous'),
            InlineKeyboardButton('About 📕', callback_data='about')
        ], [
            InlineKeyboardButton('Help 💡', callback_data='help'),
            InlineKeyboardButton('Settings ⚙', callback_data='settings')
        ], [
            InlineKeyboardButton('Open Source Repository 🌐', url='https://github.com/Ns-AnoNymouS/jiosaavn')
        ]]  
        logger.debug(f"User mention: {mention}")  
        await msg.edit(
            text=TEXT.START_MSG.format(mention=mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except KeyError as e:
        logger.error(f"Error in start command: {e}")
        await msg.edit(text="An error occurred while processing your request.")


@Bot.on_callback_query(filters.regex('^help$'))
@Bot.on_message(filters.command('help') & filters.private & filters.incoming)
async def help_handler(client: Bot, message: Message | CallbackQuery):
    buttons = [[
        InlineKeyboardButton('About 📕', callback_data='about'),
        InlineKeyboardButton('Settings ⚙', callback_data='settings')
        ],[
        InlineKeyboardButton('Home 🏕', callback_data='home'),
        InlineKeyboardButton('Close ❌', callback_data='close')
    ]]

    if isinstance(message, Message):
        await message.reply_text(text=TEX.HELP_MSG, reply_markup=InlineKeyboardMarkup(buttons), quote=True)
    else:
        await message.message.edit(text=TEX.HELP_MSG, reply_markup=InlineKeyboardMarkup(buttons))

@Bot.on_callback_query(filters.regex('^about$'))
@Bot.on_message(filters.command('about') & filters.private & filters.incoming)
async def about(client: Bot, message: Message|CallbackQuery):
    me = await client.get_me()
    buttons = [[
        InlineKeyboardButton('Help 💡', callback_data='help'),
        InlineKeyboardButton('Settings ⚙', callback_data='settings')
        ],[
        InlineKeyboardButton('Home 🏕', callback_data='home'),
        InlineKeyboardButton('Close ❌', callback_data='close')
    ]]
    if isinstance(message, Message):
        await message.reply_text(text=TEXT.ABOUT_MSG.format(me=me), reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True, quote=True)
    else:
        await message.message.edit(text=TEXT.ABOUT_MSG.format(me=me), reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

@Bot.on_callback_query(filters.regex('^close$'))
async def close_cb(client: Bot, callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await callback.message.reply_to_message.delete()
