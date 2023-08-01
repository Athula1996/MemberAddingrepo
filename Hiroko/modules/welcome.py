from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Hiroko import Hiroko

# ------------------------------------------------------------------------------- #

@Hiroko.on_message(filters.new_chat_members)
def welcome_message(client: Client, message: Message):
      chat_id = message.chat.id
      member_names = [member.first_name for member in message.new_chat_members]
       
      welcome_text = f"**ᴡᴇʟᴄᴏᴍᴇ** <b>{', '.join(member_names)}</b>!"
      welcome_text += "\n\n**ᴛʜᴀɴᴋs ғᴏʀ ᴊᴏɪɴɪɴɢ ᴏᴜʀ ᴀssᴏᴄɪᴀᴛɪᴏɴ.**"
      welcome_text += "\n***ᴘʟᴇᴀsᴇ ʀᴇᴀᴅ ɪɴ ᴛʜᴇ ᴘɪɴɴᴇᴅ ᴍᴇssᴀɢᴇ.**"
       
      button_text = "✨ ᴀssᴏᴄɪᴀᴛɪᴏɴ ✨"
      button_url = "https://t.me/TheNixaAssociation"
      wlcm_img = "https://telegra.ph/file/fea7018b5eecc877055a7.jpg"
      button = InlineKeyboardButton(button_text, url=button_url)
      markup = InlineKeyboardMarkup([[button]])
       
      client.send_photo(chat_id, photo=wlcm_img, caption=welcome_text, reply_markup=markup)


# ------------------------------------------------------------------------------- #


