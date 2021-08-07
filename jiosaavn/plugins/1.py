from pyrogram import Client


@Client.on_message()
async def addtodb(c, m):
    if not await c.db.is_user_exist(m.from_user.id):
        await c.db.add_user(m.from_user.id)
    await m.continue_propagation()


@Client.on_callback_query()
async def callback_addtodb(c, m):
    if not await c.db.is_user_exist(m.from_user.id):
        await c.db.add_user(m.from_user.id)
    await m.continue_propagation()
