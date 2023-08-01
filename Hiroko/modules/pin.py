from pyrogram import Client, filters, enums
from pyrogram.types import Message
from config import COMMAND_HANDLER
from Hiroko import Hiroko
from Hiroko.Helper.cust_p_filters import admin_filter


pinned_text = """
**ᴛʜɪs ᴍᴇssᴀɢᴇ ɪs ᴘɪɴɴᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ !**

**ᴄʜᴀᴛ:** {}
**ᴀᴅᴍɪɴ:** {}

**ᴘɪɴɴᴇᴅ: [ᴍᴇssᴀɢᴇ]({})**
"""

# ------------------------------------------------------------------------------- #

@Hiroko.on_message(filters.command("pin", COMMAND_HANDLER) & admin_filter)
def pin(_, message):
      chat = message.chat
      chat_title = message.chat.title
      chat_id = message.chat.id
      user_id = message.from_user.id
      first_name = message.from_user.first_name
      
      if message.chat.type == enums.ChatType.PRIVATE:
            return message.reply_text("**ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋ ᴏɴʟʏ ᴏɴ ɢʀᴏᴜᴘs !**")
    
      user_stats = Hiroko.get_chat_member(chat_id, user_id)
      if user_stats.privileges.can_pin_messages and not message.reply_to_message:
         
          try:
            message_id = int(message.text.split(None,1)[1])
            bot.pin_chat_message(chat_id, message_id)
            msg_link = f"t.me/{chat.username}/{message_id}"
            message.reply_text(pinned_text.format(chat_title,first_name,msg_link),disable_web_page_preview=True)
          except Exception as e:
                 return message.reply_text(str(e))

      else:
          try:
            if user_stats.privileges.can_pin_messages and message.reply_to_message:
               message.reply_to_message.pin()
               message.reply_text(pinned_text.format(chat_title,first_name, message.reply_to_message.link), disable_web_page_preview=True)
          except Exception as e:
                return message.reply_text(str(e))

unpinned_text = """
**ᴛʜɪs ᴍᴇssᴀɢᴇ ɪs ᴜɴᴘɪɴɴᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ !**

**ᴄʜᴀᴛ:** {}
**ᴀᴅᴍɪɴ:** {}

**ᴜɴᴘɪɴɴᴇᴅ: [ᴍᴇssᴀɢᴇ]({})**
"""

# ------------------------------------------------------------------------------- #

@Hiroko.on_message(filters.command("unpin", COMMAND_HANDLER) & admin_filter)
def unpin(_, message):
      chat = message.chat
      chat_title = message.chat.title
      chat_id = message.chat.id
      user_id = message.from_user.id
      first_name = message.from_user.first_name
      
      if message.chat.type == enums.ChatType.PRIVATE:
            return message.reply_text("**ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋ ᴏɴʟʏ ᴏɴ ɢʀᴏᴜᴘs !**")
    
      user_stats = Hiroko.get_chat_member(chat_id, user_id)
      if user_stats.privileges.can_pin_messages and not message.reply_to_message:
         
          try:
            message_id = int(message.text.split(None,1)[1])
            bot.unpin_chat_message(chat_id, message_id)
            msg_link = f"t.me/{chat.username}/{message_id}"
            message.reply_text(unpinned_text.format(chat_title,first_name,msg_link),disable_web_page_preview=True)
          except Exception as e:
                 return message.reply_text(str(e))

      else:
          try:
            if user_stats.privileges.can_pin_messages and message.reply_to_message:
               message.reply_to_message.unpin()
               message.reply_text(unpinned_text.format(chat_title,first_name, message.reply_to_message.link), disable_web_page_preview=True)
          except Exception as e:
                return message.reply_text(str(e))
                
# ------------------------------------------------------------------------------- #

