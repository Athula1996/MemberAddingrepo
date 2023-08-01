import requests
from Zebra import Zebra
from pyrogram import filters
from pyrogram.types import *

# --------------------------------------------------------------------------------- #

baby = InlineKeyboardMarkup([[
InlineKeyboardButton(text="sᴇɴᴅ ᴀs ғɪʟᴇ", callback_data="logo_file"),]])

# --------------------------------------------------------------------------------- #

@Zebra.on_message(filters.command("logo"))
def logo(_, message):
    global user_id, req
    user_id = message.from_user.id
    if len(message.command) <2:
       return message.reply_text("**ɢɪᴠᴇ ᴍᴇ ʟᴏɢᴏ ɴᴀᴍᴇ.**")
    logo_name = message.text.split(None,1)[1]
    msg = message.reply_text("**ʟᴏɢᴏ ɢᴇɴᴇʀᴀᴛɪɴɢ...**")
    try:
       API = f"https://api.sdbots.tk/anime-logo?name={logo_name}"
       req = requests.get(API).url
       bot.send_photo(
            message.chat.id,
            photo=req,
            caption=f"{req}",
            reply_to_message_id=message.id,reply_markup=baby)
       msg.delete()
    except Exception as e:
        msg.edit_text(str(e))
  
# --------------------------------------------------------------------------------- #
     
@Zebra.on_callback_query(filters.regex("logo_file"))
async def sendlogoasfile(_, query):
     if query.from_user.id == user_id:
        msg = await query.message.reply_text("**sᴇɴᴅɪɴɢ ғɪʟᴇ...**")
        file = await query.message.download(file_name="logo.png")
        await query.message.reply_document(
        document=file,caption=f"{req}")
        await query.message.delete()
        await msg.delete()
     else:
         await query.answer("ᴛʜɪs ᴍᴇssᴀɢᴇ ɴᴏᴛ ғᴏʀ ʏᴏᴜ !", show_alert=True)
         
# --------------------------------------------------------------------------------- #

