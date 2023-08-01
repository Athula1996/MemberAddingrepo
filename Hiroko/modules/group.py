from pyrogram import enums
from pyrogram.enums import ChatType
from pyrogram import filters, Client
from Hiroko import Hiroko
from Hiroko.Helper.cust_p_filters import admin_filter


# --------------------------------------------------------------------------------- #

@Hiroko.on_message(filters.command("removephoto")& admin_filter)
async def deletechatphoto(_, message):
      
      chat_id = message.chat.id
      user_id = message.from_user.id
      msg = await message.reply_text("ᴘʀᴏᴄᴇssɪɴɢ....")
      admin_check = await Hiroko.get_chat_member(chat_id, user_id)
      if message.chat.type == enums.ChatType.PRIVATE:
           await msg.edit("`ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋ ᴏɴ ɢʀᴏᴜᴘs !`") 
      try:
         if admin_check.privileges.can_change_info:
             await Hiroko.delete_chat_photo(chat_id)
             await msg.edit("**sᴜᴄᴄᴇssғᴜʟʟʏ ʀᴇᴍᴏᴠᴇᴅ ᴘʀᴏғɪʟᴇ ᴘʜᴏᴛᴏ ғʀᴏᴍ ɢʀᴏᴜᴘ !\nʙʏ** {}".format(message.from_user.mention))    
      except:
          await msg.edit("**ᴛʜᴇ ᴜsᴇʀ ᴍᴏsᴛ ɴᴇᴇᴅ ᴄʜᴀɴɢᴇ ɪɴғᴏ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ᴛᴏ ʀᴇᴍᴏᴠᴇ ɢʀᴏᴜᴘ ᴘʜᴏᴛᴏ !**")


# --------------------------------------------------------------------------------- #

@Hiroko.on_message(filters.command("setphoto")& admin_filter)
async def setchatphoto(_, message):
      reply = message.reply_to_message
      chat_id = message.chat.id
      user_id = message.from_user.id
      msg = await message.reply_text("ᴘʀᴏᴄᴇssɪɴɢ...")
      admin_check = await Hiroko.get_chat_member(chat_id, user_id)
      if message.chat.type == enums.ChatType.PRIVATE:
           await msg.edit("`ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋ ᴏɴ ɢʀᴏᴜᴘs !`") 
      elif not reply:
           await msg.edit("**ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴘʜᴏᴛᴏ ᴏʀ ᴅᴏᴄᴜᴍᴇɴᴛ.**")
      elif reply:
          try:
             if admin_check.privileges.can_change_info:
                photo = await reply.download()
                await message.chat.set_photo(photo=photo)
                await msg.edit_text("**sᴜᴄᴄᴇssғᴜʟʟʏ ɴᴇᴡ ᴘʀᴏғɪʟᴇ ᴘʜᴏᴛᴏ ɪɴsᴇʀᴛ !\nʙʏ** {}".format(message.from_user.mention))
             else:
                await msg.edit("`sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ʜᴀᴘᴘᴇɴᴇᴅ ᴛʀʏ ᴀɴᴏᴛʜᴇʀ ᴘʜᴏᴛᴏ !`")
     
          except:
              await msg.edit("**ᴛʜᴇ ᴜsᴇʀ ᴍᴏsᴛ ɴᴇᴇᴅ ᴄʜᴀɴɢᴇ ɪɴғᴏ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ᴘʜᴏᴛᴏ !**")


# --------------------------------------------------------------------------------- #

@Hiroko.on_message(filters.command("settitle")& admin_filter)
async def setgrouptitle(_, message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("ᴘʀᴏᴄᴇssɪɴɢ...")
    if message.chat.type == enums.ChatType.PRIVATE:
          await msg.edit("**ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋ ᴏɴ ɢʀᴏᴜᴘs !**")
    elif reply:
          try:
            title = message.reply_to_message.text
            admin_check = await Hiroko.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
               await message.chat.set_title(title)
               await msg.edit("**sᴜᴄᴄᴇssғᴜʟʟʏ ɴᴇᴡ ɢʀᴏᴜᴘ ɴᴀᴍᴇ ɪɴsᴇʀᴛ !\nʙʏ** {}".format(message.from_user.mention))
          except AttributeError:
                await msg.edit("**ᴛʜᴇ ᴜsᴇʀ ᴍᴏsᴛ ɴᴇᴇᴅ ᴄʜᴀɴɢᴇ ɪɴғᴏ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ᴛɪᴛʟᴇ !**")   
    elif len(message.command) >1:
        try:
            title = message.text.split(None, 1)[1]
            admin_check = await Hiroko.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
               await message.chat.set_title(title)
               await msg.edit("**sᴜᴄᴄᴇssғᴜʟʟʏ ɴᴇᴡ ɢʀᴏᴜᴘ ɴᴀᴍᴇ ɪɴsᴇʀᴛ !\nʙʏ** {}".format(message.from_user.mention))
        except AttributeError:
               await msg.edit("**ᴛʜᴇ ᴜsᴇʀ ᴍᴏsᴛ ɴᴇᴇᴅ ᴄʜᴀɴɢᴇ ɪɴғᴏ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ᴛɪᴛʟᴇ !**")
          

    else:
       await msg.edit("**ʏᴏᴜ ɴᴇᴇᴅ ʀᴇᴘʟʏ ᴛᴏ ᴛᴇxᴛ ᴏʀ ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ᴛɪᴛʟᴇ **")


# --------------------------------------------------------------------------------- #



# Promote a member to administrator
@app.on_message()
async def promote_member(client, message):
    if message.text == "/promote":
        chat_id = message.chat.id
        user_id = message.from_user.id
        
        # Check if the user is an admin
        admin_check = await client.get_chat_member(chat_id, user_id)
        if admin_check.status in ["creator", "administrator"]:
            # Promote the member to administrator
            await client.promote_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                can_change_info=True,
                can_delete_messages=True,
                can_invite_users=True,
                can_restrict_members=True,
                can_pin_messages=True,
                can_promote_members=False
            )
            await message.reply_text("User promoted to administrator!")
        else:
            await message.reply_text("You need to be an admin to promote members!")


# --------------------------------------------------------------------------------- #



