import time
from asyncio import sleep as rest
from pyrogram import Client, filters
from pyrogram.types import Message
from Zebra import boot as tim
from Zebra import Zebra
from Zebra import OWNER_ID as owner
from Zebra import SUDO_USERS as sudo
from pyrogram import filters, __version__
from platform import python_version


# ------------------------------------------------------------------------------- #

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


sudo.append(owner)

# ------------------------------------------------------------------------------- #

@Zebra.on_message(filters.command(["ping"], prefixes=["/", "!"]))
async def ping(Client, m: Message):
    start_time = time.time()
    sender = m.from_user
    up = get_readable_time((time.time() - tim))
    end_time = time.time()
    ping1 = str(round((end_time - start_time) * 1000, 3)) + " ms"
    if m.from_user.id in sudo:
        e = await m.reply("ɢᴇᴛᴛɪɴɢ ᴘɪɴɢɪɴɢ sᴛᴀᴛᴜs...")
        await rest(2)
        await e.edit_text("ᴘɪɴɢɪɴɢ ✨")
        await rest(1)
        await e.edit_text(PING_TEXT.format(ping1, up, __version__), ) 
       
    if m.from_user.id not in sudo:
        await m.reply(("ʏᴏᴜʀ ᴀʀᴇ ɴᴏᴛ ᴍʏ ᴍᴀsᴛᴇʀ ʜᴜʜ!!😏😏\nʙsᴅᴋ ɢᴀɴᴅ ᴘᴇ ɪᴛɴᴇ ᴛʜʜᴘᴀᴅ ᴍᴀʀᴜɴɢᴀ ᴏᴡɴᴇʀ ɢɪʀɪ ᴄʜʜᴜᴛ ᴊᴀᴀʏᴇɢɪ ʜᴜʜ 🤭 [ʟᴏᴅᴀ](tg://user?id={}) ᴘᴇʀsᴏɴ.").format(sender.id))

# ------------------------------------------------------------------------------- #

PING_TEXT = """
˹ᴢᴇʙꝛᴧ ꝛᴏʙᴏᴛ˼ 🇮🇳 sʏsᴛᴇᴍ sᴛᴀᴛs :

**ᴘɪɴɢ ᴘᴏɴɢ:** `{}`
**ʙᴏᴛ ᴜᴘᴛɪᴍᴇ:** `{}`
**ʟɪʙʀᴀʀʏ:** `ᴘʏʀᴏɢʀᴀᴍ`
**ᴍʏ ᴍᴀsᴛᴇʀ: ** `sᴜᴍɪᴛ ʏᴀᴅᴀᴠ`
**ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ:** `3.10.4`
**ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ:** `{}`
"""
# ------------------------------------------------------------------------------- #

