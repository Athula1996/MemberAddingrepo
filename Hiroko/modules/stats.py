from pyrogram import filters, Client
from pyrogram.types import Message
from config import OWNER_ID
from Hiroko import Hiroko
from Hiroko.Helper.database.chats import get_served_chats
from Hiroko.Helper.database.users import get_served_users

# --------------------------------------------------------------------------------- #

@Zebra.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def stats(cli: Client, message: Message):
    users = len(await get_served_users())
    chats = len(await get_served_chats())
    await message.reply_text(
        f"""**ᴛᴏᴛᴀʟ sᴛᴀᴛs ᴏғ **{(await cli.get_me()).mention} :

➻ **ᴄʜᴀᴛs :** {chats}
➻ **ᴜsᴇʀs :** {users}"""
    )
    
# --------------------------------------------------------------------------------- #
