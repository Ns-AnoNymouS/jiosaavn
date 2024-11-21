import logging
import asyncio
import random
from jiosaavn.bot import Bot
from jiosaavn.plugins.text import TEXT
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

logger = logging.getLogger(__name__)

# Helper function to handle reactions and message editing
async def send_reaction_and_edit(client, message, msg_text, buttons):
    random_emoji = random.choice(TEXT.EMOJI_LIST)
    # Send reaction only for commands (not for every message)
    await client.send_reaction(
        chat_id=message.chat.id,
        message_id=message.id,
        emoji=random_emoji,
        big=True
    )
    await asyncio.sleep(0.5)  # Optional delay for better UI experience
    await message.edit(
        text=msg_text,
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )

# Start Command
@Bot.on_callback_query(filters.regex('^home$'))
@Bot.on_message(filters.command('start') & filters.private & filters.incoming)
async def start(c, m):
    last_name = f' {m.from_user.last_name}' if m.from_user.last_name else ''
    mention = f"[{m.from_user.first_name}{last_name}](tg://user?id={m.from_user.id})" if m.from_user.first_name else f"[User](tg://user?id={m.from_user.id})"
    
    buttons = [
        [InlineKeyboardButton('Owner 🧑', url='https://t.me/Ns_AnoNymous'),
         InlineKeyboardButton('About 📕', callback_data='about')],
        [InlineKeyboardButton('Help 💡', callback_data='help'),
         InlineKeyboardButton('Settings ⚙', callback_data='settings')],
        [InlineKeyboardButton('Open Source Repository 🌐', url='https://github.com/Ns-AnoNymouS/jiosaavn')],
        [InlineKeyboardButton('Close ❌', callback_data='close')]
    ]

    await send_reaction_and_edit(c, m, TEXT.START_MSG.format(mention=mention), buttons)

# Help Command
@Bot.on_callback_query(filters.regex('^help$'))
@Bot.on_message(filters.command('help') & filters.private & filters.incoming)
async def help_handler(client: Bot, message: Message | CallbackQuery):
    buttons = [
        [InlineKeyboardButton('About 📕', callback_data='about'),
         InlineKeyboardButton('Settings ⚙', callback_data='settings')],
        [InlineKeyboardButton('Home 🏕', callback_data='home'),
         InlineKeyboardButton('Close ❌', callback_data='close')]
    ]
    await send_reaction_and_edit(client, message, TEXT.HELP_MSG, buttons)

# About Command
@Bot.on_callback_query(filters.regex('^about$'))
@Bot.on_message(filters.command('about') & filters.private & filters.incoming)
async def about(client: Bot, message: Message | CallbackQuery):
    try:
        me = await client.get_me()
        buttons = [
            [InlineKeyboardButton('Help 💡', callback_data='help'),
             InlineKeyboardButton('Settings ⚙', callback_data='settings')],
            [InlineKeyboardButton('Home 🏕', callback_data='home'),
             InlineKeyboardButton('Close ❌', callback_data='close')]
        ]
        await send_reaction_and_edit(client, message, TEXT.ABOUT_MSG.format(me=me), buttons)
    except Exception as e:
        logger.error(f"Error in about command: {e}")
        await message.edit("An error occurred while processing your request.")

# Close Command
@Bot.on_callback_query(filters.regex('^close$'))
async def close_cb(client: Bot, callback: CallbackQuery):
    try:
        await callback.answer()
        await callback.message.delete()
        if callback.message.reply_to_message:
            await callback.message.reply_to_message.delete()
    except Exception as e:
        logger.error(f"Error in close_cb command: {e}")
        await callback.message.edit("An error occurred while closing the message.")
        
