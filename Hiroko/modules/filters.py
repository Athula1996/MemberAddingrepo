import os
import re
import io
from config import OWNER_ID
import asyncio
import pyrogram
from Hiroko import Hiroko
from pyrogram import filters, Client, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Hiroko.Helper.database.connection_db import active_connection
from Hiroko.Helper.database.users_db import add_user, all_users
from Hiroko.Helper.utils import parser,split_quotes
from Hiroko.Helper.database.filters_db import(
   add_filter,
   find_filter,
   get_filters,
   delete_filter,
   count_filters
)

SAVE_USER = os.environ.get("SAVE_USER", "no").lower()

# ====================> ғɪʟᴛᴇʀ <==================== #

@Hiroko.on_message(filters.command("filter"))
async def addfilter(client, message):
      
    userid = message.from_user.id
    chat_type = message.chat.type
    args = message.text.html.split(None, 1)

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("ᴍᴀᴋᴇ sᴜʀᴇ ɪ'ᴍ ᴘʀᴇsᴇɴᴛ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ !!", quote=True)
                return
        else:
            await message.reply_text("ɪ'ᴍ ɴᴏᴛ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ ᴀɴʏ ɢʀᴏᴜᴘ!", quote=True)
            return

    elif (chat_type == enums.ChatType.GROUP) or (chat_type == enums.ChatType.SUPERGROUP):
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if not ((st.status == enums.ChatMemberStatus.ADMINISTRATOR) or (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in OWNER_ID)):
        return
        

    if len(args) < 2:
        await message.reply_text("ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ɢɪᴠᴇ ᴛʜᴇ ғɪʟᴛᴇʀ ᴀ ɴᴀᴍᴇ ! ", quote=True)
        return
    
    extracted = split_quotes(args[1])
    text = extracted[0].lower()
   
    if not message.reply_to_message and len(extracted) < 2:
        await message.reply_text("ᴀᴅᴅ sᴏᴍᴇ ᴄᴏɴᴛᴇɴᴛ ᴛᴏ sᴀᴠᴇ ʏᴏᴜʀ ғɪʟᴛᴇʀ !", quote=True)
        return

    if (len(extracted) >= 2) and not message.reply_to_message:
        reply_text, btn, alert = parser(extracted[1], text)
        fileid = None
        if not reply_text:
            await message.reply_text("ʏᴏᴜ ᴄᴀɴɴᴏᴛ ʜᴀᴠᴇ ʙᴜᴛᴛᴏɴs ᴀʟᴏɴᴇ, ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ɢᴏ ᴡɪᴛʜ ɪᴛ !", quote=True)
            return

    elif message.reply_to_message and message.reply_to_message.reply_markup:
        try:
            rm = message.reply_to_message.reply_markup
            btn = rm.inline_keyboard
            msg = message.reply_to_message.document or\
                  message.reply_to_message.video or\
                  message.reply_to_message.photo or\
                  message.reply_to_message.audio or\
                  message.reply_to_message.animation or\
                  message.reply_to_message.sticker
            if msg:
                fileid = msg.file_id
                reply_text = message.reply_to_message.caption.html
            else:
                reply_text = message.reply_to_message.text.html
                fileid = None
            alert = None
        except:
            reply_text = ""
            btn = "[]" 
            fileid = None
            alert = None

    elif message.reply_to_message and message.reply_to_message.photo:
        try:
            fileid = message.reply_to_message.photo.file_id
            reply_text, btn, alert = parser(message.reply_to_message.caption.html, text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None

    elif message.reply_to_message and message.reply_to_message.video:
        try:
            fileid = message.reply_to_message.video.file_id
            reply_text, btn, alert = parser(message.reply_to_message.caption.html, text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None

    elif message.reply_to_message and message.reply_to_message.audio:
        try:
            fileid = message.reply_to_message.audio.file_id
            reply_text, btn, alert = parser(message.reply_to_message.caption.html, text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None
   
    elif message.reply_to_message and message.reply_to_message.document:
        try:
            fileid = message.reply_to_message.document.file_id
            reply_text, btn, alert = parser(message.reply_to_message.caption.html, text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None

    elif message.reply_to_message and message.reply_to_message.animation:
        try:
            fileid = message.reply_to_message.animation.file_id
            reply_text, btn, alert = parser(message.reply_to_message.caption.html, text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None

    elif message.reply_to_message and message.reply_to_message.sticker:
        try:
            fileid = message.reply_to_message.sticker.file_id
            reply_text, btn, alert =  parser(extracted[1], text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None

    elif message.reply_to_message and message.reply_to_message.text:
        try:
            fileid = None
            reply_text, btn, alert = parser(message.reply_to_message.text.html, text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None

    else:
        return
    
    await add_filter(grp_id, text, reply_text, btn, fileid, alert)

    await message.reply_text(
        f"ғɪʟᴛᴇʀ ғᴏʀ  `{text}`  ᴀᴅᴅᴇᴅ ɪɴ  **{title}**",
        quote=True,
        parse_mode=enums.ParseMode.MARKDOWN
    )



# ====================> ғɪʟᴛᴇʀs <==================== #

@Hiroko.on_message(filters.command("filters"))
async def get_all(client, message):
    
    chat_type = message.chat.type
    userid = message.from_user.id
    if chat_type == enums.ChatType.PRIVATE:
        
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("ᴍᴀᴋᴇ sᴜʀᴇ ɪ'ᴍ ᴘʀᴇsᴇɴᴛ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ !!", quote=True)
                return
        else:
            await message.reply_text("ɪ'ᴍ ɴᴏᴛ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ ᴀɴʏ ɢʀᴏᴜᴘ !", quote=True)
            return

    elif (chat_type == enums.ChatType.GROUP) or (chat_type == enums.ChatType.SUPERGROUP):
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if not ((st.status == enums.ChatMemberStatus.ADMINISTRATOR) or (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in OWNER_ID)):
        return

    texts = await get_filters(grp_id)
    count = await count_filters(grp_id)
    if count:
        filterlist = f"ᴛᴏᴛᴀʟ ɴᴜᴍʙᴇʀ ᴏғ ғɪʟᴛᴇʀs ɪɴ **{title}** : {count}\n\n"

        for text in texts:
            keywords = " •×  `{}`\n".format(text)
            
            filterlist += keywords

        if len(filterlist) > 4096:
            with io.BytesIO(str.encode(filterlist.replace("`", ""))) as keyword_file:
                keyword_file.name = "keywords.txt"
                await message.reply_document(
                    document=keyword_file,
                    quote=True
                )
            return
    else:
        filterlist = f"ᴛʜᴇʀᴇ ᴀʀᴇ ɴᴏ ᴀᴄᴛɪᴠᴇ ғɪʟᴛᴇʀs ɪɴ **{title}**"

    await message.reply_text(
        text=filterlist,
        quote=True,
        parse_mode=enums.ParseMode.MARKDOWN
    )
 

# ====================> ᴅᴇʟᴇᴛᴇ-ғɪʟᴛᴇʀs <==================== #
       
@Hiroko.on_message(filters.command("del"))
async def deletefilter(client, message):
    userid = message.from_user.id
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid  = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("ᴍᴀᴋᴇ sᴜʀᴇ ɪ'ᴍ ᴘʀᴇsᴇɴᴛ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ !!", quote=True)
                return
        else:
            await message.reply_text("ɪ'ᴍ ɴᴏᴛ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ ᴀɴʏ ɢʀᴏᴜᴘ !", quote=True)

    elif (chat_type == enums.ChatType.GROUP) or (chat_type == enums.ChatType.SUPERGROUP):
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if not ((st.status == enums.ChatMemberStatus.ADMINISTRATOR) or (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in OWNER_ID)):
        return

    try:
        cmd, text = message.text.split(" ", 1)
    except:
        await message.reply_text(
            "<i>ᴍᴇɴᴛɪᴏɴ ᴛʜᴇ ғɪʟᴛᴇʀ ɴᴀᴍᴇ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴɴᴀ ᴅᴇʟᴇᴛᴇ !</i>\n\n"
            "<code>/del ғɪʟᴛᴇʀ ɴᴀᴍᴇ</code>\n\n"
            "ᴜsᴇ /filters ᴛᴏ ᴠɪᴇᴡ ᴀʟʟ ᴀᴠᴀɪʟᴀʙʟᴇ ғɪʟᴛᴇʀs",
            quote=True
        )
        return

    query = text.lower()

    await delete_filter(message, query, grp_id)
        


# ====================> ᴅᴇʟᴇᴛᴇ-ᴀʟʟ-ғɪʟᴛᴇʀs <==================== #

@Hiroko.on_message(filters.command("delall"))
async def delallconfirm(client, message):
    userid = message.from_user.id
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid  = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("ᴍᴀᴋᴇ sᴜʀᴇ ɪ'ᴍ ᴘʀᴇsᴇɴᴛ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ !!", quote=True)
                return
        else:
            await message.reply_text("ɪ'ᴍ ɴᴏᴛ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ ᴀɴʏ ɢʀᴏᴜᴘ !", quote=True)
            return

    elif (chat_type == enums.ChatType.GROUP) or (chat_type == enums.ChatType.SUPERGROUP):
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in OWNER_ID):
        await message.reply_text(
            f"ᴛʜɪs ᴡɪʟʟ ᴅᴇʟᴇᴛᴇ ᴀʟʟ ғɪʟᴛᴇʀs ғʀᴏᴍ '{title}'.\nᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ !!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text="ʏᴇs",callback_data="delallconfirm")],
                [InlineKeyboardButton(text="ᴄᴀɴᴄᴇʟ",callback_data="delallcancel")]
            ]),
            quote=True
        )



# ====================> ɢɪᴠᴇ-ғɪʟᴛᴇʀs <==================== #

@Hiroko.on_message((filters.private | filters.group) & filters.text)
async def give_filter(client,message):
    group_id = message.chat.id
    name = message.text

    keywords = await get_filters(group_id)
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_filter(group_id, keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            rk = await message.reply_text(reply_text, disable_web_page_preview=True)
                            await asyncio.sleep(30)
                            await rk.delete()
                        else:
                            button = eval(btn)
                            rk = await message.reply_text(
                                 reply_text,
                                 disable_web_page_preview=True,
                                 reply_markup=InlineKeyboardMarkup(button)
                            )
                            await asyncio.sleep(30)
                            await rk.delete()
                    else:
                        if btn == "[]":
                            rk = await message.reply_cached_media(
                                 fileid,
                                 caption=reply_text or ""
                            )
                            await asyncio.sleep(30)
                            await rk.delete()
                        else:
                            button = eval(btn) 
                            rk = await message.reply_cached_media(
                                 fileid,
                                 caption=reply_text or "",
                                 reply_markup=InlineKeyboardMarkup(button)
                            )
                            await asyncio.sleep(30)
                            await rk.delete()
                except Exception as e:
                    print(e)
                    pass
                break 
                
    if SAVE_USER == "yes":
        try:
            await add_user(
                str(message.from_user.id),
                str(message.from_user.username),
                str(message.from_user.first_name + " " + (message.from_user.last_name or "")),
                str(message.from_user.dc_id)
            )
        except:
            pass
      
