import logging
import asyncio
import random
from jiosaavn.bot import Bot
from pyrogram import filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import MessageNotModified, RPCError

logger = logging.getLogger(__name__)

DEFAULT_EMOJI_LIST = ["👍", "👎", "😊", "😢", "😍", "🔥", "🎉"]

@Bot.on_callback_query(filters.regex('^home$'))
@Bot.on_message(filters.command('start') & filters.private & filters.incoming)
async def start(c: Bot, m: Message | CallbackQuery):
    try:
        from jiosaavn.plugins.text import TEXT
        start_msg = TEXT.START_MSG
    except (ImportError, AttributeError) as e:
        logger.warning(f"Failed to access TEXT.START_MSG: {e}. Using default message.")
        start_msg = "Welcome to the JioSaavn Bot! 🎵\n\nUse /search to find songs, albums, or playlists.\n\n{mention}"

    last_name = f' {m.from_user.last_name}' if m.from_user.last_name else ''
    mention = f"[{m.from_user.first_name}{last_name}](tg://user?id={m.from_user.id})" if m.from_user.first_name else f"[User](tg://user?id={m.from_user.id})"    
    msg = m.message if getattr(m, "data", None) else await m.reply("**Processing....⌛**", quote=True)
    
    buttons = [
        [InlineKeyboardButton('Owner 🧑', url='https://t.me/The_proGrammerr'),
         InlineKeyboardButton('About 📕', callback_data='about')],
        [InlineKeyboardButton('Help 💡', callback_data='help'),
         InlineKeyboardButton('Settings ⚙', callback_data='settings')],
        [InlineKeyboardButton('Open Source Repository 🌐', url='https://github.com/Ns-AnoNymouS/jiosaavn')],
        [InlineKeyboardButton('Close ❌', callback_data='close')]
    ]
    
    text = start_msg.format(mention=mention)
    
    # Add reaction to user's command message (only for Message, not CallbackQuery)
    if isinstance(m, Message):
        try:
            emoji = random.choice(DEFAULT_EMOJI_LIST)
            await c.send_reaction(
                chat_id=m.chat.id,
                message_id=m.id,
                emoji=emoji,
                big=False
            )
            logger.info(f"Added {emoji} reaction to /start message {m.id} for user {m.from_user.id}")
        except RPCError as e:
            logger.error(f"Failed to send reaction to /start: {e}")
        except Exception as e:
            logger.error(f"Unexpected error sending reaction to /start: {e}")
    
    try:
        if msg.text != text or msg.reply_markup != InlineKeyboardMarkup(buttons):
            await msg.edit(
                text=text,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            logger.debug(f"Edited start message for user {m.from_user.id}")
        else:
            logger.debug(f"Skipped redundant edit for start message")
    except MessageNotModified:
        logger.warning("Message not modified in start command")
    except Exception as e:
        logger.error(f"Error in start command: {e}")
        await msg.edit("An error occurred while processing your request.")

@Bot.on_callback_query(filters.regex('^help$'))
@Bot.on_message(filters.command('help') & filters.private & filters.incoming)
async def help_handler(client: Bot, message: Message | CallbackQuery):
    try:
        from jiosaavn.plugins.text import TEXT
        help_msg = TEXT.HELP_MSG
    except (ImportError, AttributeError) as e:
        logger.warning(f"Failed to access TEXT.HELP_MSG: {e}. Using default message.")
        help_msg = "Help for JioSaavn Bot:\n\n- /start: Start the bot\n- /search <query>: Search for songs, albums, or playlists\n- /settings: Configure search type and audio quality\n- /about: About the bot"

    msg = message.message if getattr(message, "data", None) else await message.reply("**Processing....⌛**", quote=True)
    buttons = [
        [InlineKeyboardButton('About 📕', callback_data='about'),
         InlineKeyboardButton('Settings ⚙', callback_data='settings')],
        [InlineKeyboardButton('Home 🏕', callback_data='home'),
         InlineKeyboardButton('Close ❌', callback_data='close')]
    ]
    
    # Add reaction to user's command message (only for Message, not CallbackQuery)
    if isinstance(message, Message):
        try:
            emoji = random.choice(DEFAULT_EMOJI_LIST)
            await client.send_reaction(
                chat_id=message.chat.id,
                message_id=message.id,
                emoji=emoji,
                big=False
            )
            logger.info(f"Added {emoji} reaction to /help message {message.id} for user {message.from_user.id}")
        except RPCError as e:
            logger.error(f"Failed to send reaction to /help: {e}")
        except Exception as e:
            logger.error(f"Unexpected error sending reaction to /help: {e}")
    
    try:
        if msg.text != help_msg or msg.reply_markup != InlineKeyboardMarkup(buttons):
            await msg.edit(
                text=help_msg,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            logger.debug(f"Edited help message for user {message.from_user.id}")
        else:
            logger.debug(f"Skipped redundant edit for help message")
    except MessageNotModified:
        logger.warning("Message not modified in help_handler")
    except Exception as e:
        logger.error(f"Error in help_handler command: {e}")
        await msg.edit("An error occurred while processing your request.")

@Bot.on_callback_query(filters.regex('^about$'))
@Bot.on_message(filters.command('about') & filters.private & filters.incoming)
async def about(client: Bot, message: Message | CallbackQuery):
    try:
        from jiosaavn.plugins.text import TEXT
        about_msg = TEXT.ABOUT_MSG
    except (ImportError, AttributeError) as e:
        logger.warning(f"Failed to access TEXT.ABOUT_MSG: {e}. Using default message.")
        about_msg = "JioSaavn Bot\n\nA Telegram bot to search and download music from JioSaavn.\n\nBot: @{me.username}\nOwner: @The_proGrammerr"

    msg = message.message if getattr(message, "data", None) else await message.reply("**Processing....⌛**", quote=True)
    me = await client.get_me()
    buttons = [
        [InlineKeyboardButton('Help 💡', callback_data='help'),
         InlineKeyboardButton('Settings ⚙', callback_data='settings')],
        [InlineKeyboardButton('Home 🏕', callback_data='home'),
         InlineKeyboardButton('Close ❌', callback_data='close')]
    ]
    
    text = about_msg.format(me=me)
    
    # Add reaction to user's command message (only for Message, not CallbackQuery)
    if isinstance(message, Message):
        try:
            emoji = random.choice(DEFAULT_EMOJI_LIST)
            await client.send_reaction(
                chat_id=message.chat.id,
                message_id=message.id,
                emoji=emoji,
                big=False
            )
            logger.info(f"Added {emoji} reaction to /about message {message.id} for user {message.from_user.id}")
        except RPCError as e:
            logger.error(f"Failed to send reaction to /about: {e}")
        except Exception as e:
            logger.error(f"Unexpected error sending reaction to /about: {e}")
    
    try:
        if msg.text != text or msg.reply_markup != InlineKeyboardMarkup(buttons):
            await msg.edit(
                text=text,
                reply_markup=InlineKeyboardMarkup(buttons),
                disable_web_page_preview=True
            )
            logger.debug(f"Edited about message for user {message.from_user.id}")
        else:
            logger.debug(f"Skipped redundant edit for about message")
    except MessageNotModified:
        logger.warning("Message not modified in about command")
    except Exception as e:
        logger.error(f"Error in about command: {e}")
        await msg.edit("An error occurred while processing your request.")

@Bot.on_callback_query(filters.regex('^close$'))
async def close_cb(client: Bot, callback: CallbackQuery):
    try:
        await callback.answer()
        await callback.message.delete()
        if callback.message.reply_to_message:
            await callback.message.reply_to_message.delete()
    except MessageNotModified:
        logger.warning("Message not modified in close_cb")
    except Exception as e:
        logger.error(f"Error in close_cb command: {e}")
        await callback.message.edit("An error occurred while closing the message.")
