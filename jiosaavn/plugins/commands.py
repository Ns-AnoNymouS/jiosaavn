from pyrogram import Client, filters


@Client.on_message(filters.command('start') & filters.private & filters.incoming)
async def start(c, m):
    text = f"Hi {m.from_user.mention(style='md')},\n\nI am a telegram jiosaavn bot helps you to search and download songs from jiosaavn.\n\n**Maintained By:** [Anonymous](https://t.me/Ns_AnoNymous)"
    await m.reply_text()
