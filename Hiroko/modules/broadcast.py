import asyncio
from config import OWNER_ID
from Hiroko import Hiroko
from pyrogram import filters
from Hiroko.Helper.database.chatsdb import *
from Hiroko.Helper.database.usersdb import *
from pyrogram.errors import FloodWait 
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

USER = []


@Hiroko.on_message(filters.command(["bcast", "broadcast"]) & filters.user([OWNER_ID]))
async def _bcast(app, message):
    replied = message.reply_to_message
    user_id = message.from_user.id
   # if user_id not in 'OWNERS':
      #  return
    if replied:
        x = replied.id
        y = message.chat.id
    else:
        if len(message.command) < 2:
            return await message.reply_text("**ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ ᴍᴇ sᴏᴍᴇᴛʜɪɴɢ ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ**")
        query = message.text.split(maxsplit=1)[1]
        if "-pin" in query:
            query = query.replace("-pin", "")
        if "-nobot" in query:
            query = query.replace("-nobot", "")
        if "-pinloud" in query:
            query = query.replace("-pinloud", "")
        if "-assistant" in query:
            query = query.replace("-assistant", "")
        if "-user" in query:
            query = query.replace("-user", "")   
        if query == "":
            return await message.reply_text("ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ")
        
    btn = InlineKeyboardMarkup([[InlineKeyboardButton("ᴄᴀɴᴄᴇʟ ʙʀᴏᴀᴅᴄᴀsᴛ", callback_data=f"cancelbcast_{user_id}")]])
    
    msg = await message.reply("ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ..........",reply_markup=btn)
    USER.append(user_id)
    if "-nobot" not in message.text:
        sent = 0
        pin = 0
        chats = await get_served_chats()
        for i in chats:
            if user_id not in USER:
                break           
            try:
                m = (
                    await app.forward_messages(i, y, x)
                    if message.reply_to_message
                    else await app.send_message(i, text=query)
                )
                if "-pin" in message.text:
                    try:
                        await m.pin(disable_notification=True)
                        pin += 1
                    except Exception:
                        continue
                elif "-pinloud" in message.text:
                    try:
                        await m.pin(disable_notification=False)
                        pin += 1
                    except Exception:
                        continue
                sent += 1
            except FloodWait as e:                
                await asyncio.sleep(e.value)
            except Exception:
                continue
        try:
            await msg.edit_text(f"ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇ ɪɴ {sent}  ᴄʜᴀᴛs ᴡɪᴛʜ {pin} ᴘɪɴs ꜰʀᴏᴍ ʙᴏᴛ")
        except:
            pass

    elif "-user" in message.text:
        susr = 0
        served_users = []
        susers = await get_served_users()
        for i in served_users:
            if user_id not in USER:
                break
            try:
                m = (
                    await app.forward_messages(i, y, x)
                    if message.reply_to_message
                    else await app.send_message(i, text=query)
                )
                susr += 1
            except FloodWait as e:                
                await asyncio.sleep(e.value)
            except Exception:
                pass
        try:
            await msg.edit("ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇ ᴛᴏ {susr} ᴜsᴇʀs")
        except:
            pass 
    else:
        chats = await get_served_chats() + await get_served_users() 
        for i in chats:
            if user_id not in USER:
                break
            try:
                m = (
                    await app.forward_messages(i, y, x)
                    if message.reply_to_message
                    else await app.send_message(i, text=query)
                )
                susr += 1
            except FloodWait as e:                
                await asyncio.sleep(e.value)
            except Exception:
                pass
        try:
            await msg.edit("ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇ ᴛᴏ {susr} chats")
        except:
            pass 
    try:
        USER.remove(user_id)
    except:
        pass
        
@Hiroko.on_callback_query(filters.regex(pattern=r"cancelbcast_(.*)"))
async def _cancelbcast(_, query):
    user_id = query.from_user.id
    if user_id != int(query.data.split("_")[1]):
        return await _.answer_callback_query(query.id,text="ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴡᴏʀᴛʜʏ sᴏɴ",show_alert=True)
    if user_id not in USER:
        return await _.answer_callback_query(query.id,text="ɪ ᴀᴍ ɴᴏᴛ ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ᴀɴʏᴛʜɪɴɢ",show_alert=True)
    try:
        USER.remove(user_id)
        await query.message.edit_text("sᴛᴏᴘᴘᴇᴅ ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ᴛʜᴇ ᴍᴇssᴀɢᴇ")
    except Exception as e:
        print(e)

      
    

                            
