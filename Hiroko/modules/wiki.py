import wikipedia
from config import COMMAND_HANDLER
from pyrogram import filters
from Hiroko import Hiroko
from pyrogram.enums import ParseMode

# ------------------------------------------------------------------------------- #

@Hiroko.on_message(filters.command("wiki",COMMAND_HANDLER))
async def wikipediasearch(_, message):
    reply = message.reply_to_message
    if len(message.command) < 2:
          await message.reply_text("**ᴇxᴀᴍᴘʟᴇ**:\n`/wiki telegram`")
          return 
    query = (
        message.text.split(None, 1)[1]
        if len(message.command) < 3
        else message.text.split(None, 1)[1].replace(" ", "%20")
    )
    if not query:
        await message.reply_text("**ɪɴᴠᴀʟɪᴅ sʏɴᴛᴀx sᴇᴇ ʜᴇʟᴘ ᴍᴇɴᴜ ᴛᴏ ᴋɴᴏᴡ ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.**")
        return
    msg = await message.reply_text("**sᴇᴀʀᴄʜɪɴɢ...**")
    results = wikipedia.search(query)
    result = ""
    for s in results:
        try:
            page = wikipedia.page(s)
            url = page.url
            result += f"𒊹︎︎︎[{s}]({url}) \n"
        except BaseException:
            pass
    await message.reply_text(
        "**ᴡɪᴋɪᴘᴇᴅɪᴀ sᴇᴀʀᴄʜ: {}** \n\n**ʀᴇsᴜʟᴛ:**\n{}".format(query, result), disable_web_page_preview=True)
    await msg.delete()
    
# ------------------------------------------------------------------------------- #

