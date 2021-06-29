import logging
logger = logging.getLogger(__name__)
from pyrogram.errors import FloodWait


async def send_audio(c, chat_id, audio, caption, duration, title, thumb, artists, reply_to_message_id):
    try:
        song = await c.send_audio(
            chat_id=chat_id,
            audio=audio,
            caption=caption,
            duration=duration,
            title=title,
            thumb=thumb,
            performer=artists,
            parse_mode="markdown",
            reply_to_message_id=reply_to_message_id
        )
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await send_audio(c, chat_id, audio, caption, duration, title, thumb, artists, reply_to_message_id)
    except Exception as e:
        logger.warning(e)
    
