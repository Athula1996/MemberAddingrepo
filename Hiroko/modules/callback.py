import os
import ast
from config import OWNER_ID
import asyncio
import random
from time import time
from datetime import datetime
from pyrogram import filters
from pyrogram import Client, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Hiroko.Helper.database.filters_db import del_all, find_filter
from Hiroko.Helper.database.connection_db import(
    all_connections,
    active_connection,
    if_active,
    delete_connection,
    make_active,
    make_inactive
)

# -----------------» ʜᴇʟᴘ-ᴍsɢ «------------------ #

HELP_MSG = """
<b> ғɪʟᴛᴇʀs ᴄᴏᴍᴍᴀɴᴅ </b>

<code>/filter ɴᴀᴍᴇ ᴏʀ ʀᴇᴘʟʏ</code>  -  <code>ᴀᴅᴅ ғɪʟᴛᴇʀ ғᴏʀ ɴᴀᴍᴇ.</code>

<code>/del ғɪʟᴛᴇʀ ɴᴀᴍᴇ</code>  -  <code>ᴅᴇʟᴇᴛᴇ ғɪʟᴛᴇʀ.</code> 

<code>/delall</code>  -  <code>ᴅᴇʟᴇᴛᴇ ᴇɴᴛɪʀᴇ ғɪʟᴛᴇʀs (ɢʀᴏᴜᴘ ᴏᴡɴᴇʀ ᴏɴʟʏ !)</code>

<code>/filters</code>  -  <code>ʟɪsᴛ ᴀʟʟ ғɪʟᴛᴇʀs ɪɴ ᴄʜᴀᴛ.</code>


<b> ᴄᴏɴɴᴇᴄᴛɪᴏɴ ᴄᴏᴍᴍᴀɴᴅs </b>

<code>/connect ɢʀᴏᴜᴘ ɪᴅ</code>  -  <code>ᴄᴏɴɴᴇᴄᴛ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴛᴏ ᴍʏ ᴘᴍ. ʏᴏᴜ ᴄᴀɴ ᴀʟsᴏ sɪᴍᴘʟᴇ.</code>

<code>/connect</code> <code>ɪɴ ɢʀᴏᴜᴘs.</code>

<code>/connections</code>  -  <code> ᴍᴀɴᴀɢᴇ ʏᴏᴜ ᴄᴏɴɴᴇᴄᴛɪᴏɴs.</code>

"""





@Client.on_callback_query()
async def cb_handler(client, query):

    if query.data == "close_data":
        await query.message.delete()
        

    elif query.data == "delallconfirm":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            grpid  = await active_connection(str(userid))
            if grpid is not None:
                grp_id = grpid
                try:
                    chat = await client.get_chat(grpid)
                    title = chat.title
                except:
                    await query.message.edit_text("ᴍᴀᴋᴇ sᴜʀᴇ ɪ'ᴍ ᴘʀᴇsᴇɴᴛ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ !!", quote=True)
                    return
            else:
                await query.message.edit_text(
                    "ɪ'ᴍ ɴᴏᴛ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ ᴀɴʏ ɢʀᴏᴜᴘs !\nᴄʜᴇᴄᴋ /connections ᴏʀ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ ᴀɴʏ ɢʀᴏᴜᴘs",
                    quote=True
                )
                return

        elif (chat_type == enums.ChatType.GROUP) or (chat_type == enums.ChatType.SUPERGROUP):
            grp_id = query.message.chat.id
            title = query.message.chat.title

        else:
            return

        st = await client.get_chat_member(grp_id, userid)
        if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in OWNER_ID):    
            await del_all(query.message, grp_id, title)
        else:
            await query.answer("ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ɢʀᴏᴜᴘ ᴏᴡɴᴇʀ ᴏʀ ᴀɴ ᴀᴜᴛʜ ᴜsᴇʀ ᴛᴏ ᴅᴏ ᴛʜᴀᴛ !",show_alert=True)
    
    elif query.data == "delallcancel":
        userid = query.from_user.id
        chat_type = query.message.chat.type
        
        if chat_type == enums.ChatType.PRIVATE:
            await query.message.reply_to_message.delete()
            await query.message.delete()

        elif (chat_type == enums.ChatType.GROUP) or (chat_type == enums.ChatType.SUPERGROUP):
            grp_id = query.message.chat.id
            st = await client.get_chat_member(grp_id, userid)
            if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in OWNER_ID):
                await query.message.delete()
                try:
                    await query.message.reply_to_message.delete()
                except:
                    pass
            else:
                await query.answer("ᴛʜᴀᴛs ɴᴏᴛ ғᴏʀ ʏᴏᴜ !!",show_alert=True)


    elif "groupcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]
        title = query.data.split(":")[2]
        act = query.data.split(":")[3]
        user_id = query.from_user.id

        if act == "":
            stat = "CONNECT"
            cb = "connectcb"
        else:
            stat = "DISCONNECT"
            cb = "disconnect"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{stat}", callback_data=f"{cb}:{group_id}:{title}"),
                InlineKeyboardButton("ᴅᴇʟᴇᴛᴇ", callback_data=f"deletecb:{group_id}")],
            [InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="backcb")]
        ])

        await query.message.edit_text(
            f"ɢʀᴏᴜᴘ ɴᴀᴍᴇ : **{title}**\nɢʀᴏᴜᴘ ɪᴅ : `{group_id}`",
            reply_markup=keyboard,
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return

    elif "connectcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]
        title = query.data.split(":")[2]
        user_id = query.from_user.id

        mkact = await make_active(str(user_id), str(group_id))

        if mkact:
            await query.message.edit_text(
                f"ᴛʜᴇ ғɪʟᴛᴇʀs ʙᴏᴛ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ **{title}**",
                parse_mode=enums.ParseMode.MARKDOWN
            )
            return
        else:
            await query.message.edit_text(
                f"sᴏᴍᴇ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ !!",
                parse_mode=enums.ParseMode.MARKDOWN
            )
            return

    elif "disconnect" in query.data:
        await query.answer()

        title = query.data.split(":")[2]
        user_id = query.from_user.id

        mkinact = await make_inactive(str(user_id))

        if mkinact:
            await query.message.edit_text(
                f"ᴛʜᴇ ғɪʟᴛᴇʀs ʙᴏᴛ ᴅɪsᴄᴏɴɴᴇᴄᴛᴇᴅ ғʀᴏᴍ **{title}**",
                parse_mode=enums.ParseMode.MARKDOWN
            )
            return
        else:
            await query.message.edit_text(
                f"sᴏᴍᴇ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ !!",
                parse_mode=enums.ParseMode.MARKDOWN
            )
            return
    elif "deletecb" in query.data:
        await query.answer()

        user_id = query.from_user.id
        group_id = query.data.split(":")[1]

        delcon = await delete_connection(str(user_id), str(group_id))

        if delcon:
            await query.message.edit_text(
                "sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ ᴄᴏɴɴᴇᴄᴛɪᴏɴ"
            )
            return
        else:
            await query.message.edit_text(
                f"sᴏᴍᴇ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ !!",
                parse_mode=enums.ParseMode.MARKDOWN
            )
            return
    
    elif query.data == "backcb":
        await query.answer()

        userid = query.from_user.id

        groupids = await all_connections(str(userid))
        if groupids is None:
            await query.message.edit_text(
                "ᴛʜᴇʀᴇ ᴀʀᴇ ɴᴏ ᴀᴄᴛɪᴠᴇ ᴄᴏɴɴᴇᴄᴛɪᴏɴs !! ᴄᴏɴɴᴇᴄᴛ ᴛᴏ sᴏᴍᴇ ɢʀᴏᴜᴘs ғɪʀsᴛ.",
            )
            return
        buttons = []
        for groupid in groupids:
            try:
                ttl = await client.get_chat(int(groupid))
                title = ttl.title
                active = await if_active(str(userid), str(groupid))
                if active:
                    act = " - ACTIVE"
                else:
                    act = ""
                buttons.append(
                    [
                        InlineKeyboardButton(
                            text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{title}:{act}"
                        )
                    ]
                )
            except:
                pass
        if buttons:
            await query.message.edit_text(
                "ʏᴏᴜʀ ᴄᴏɴɴᴇᴄᴛᴇᴅ ɢʀᴏᴜᴘ ᴅᴇᴛᴀɪʟs\n\n",
                reply_markup=InlineKeyboardMarkup(buttons)
            )

    elif "alertmessage" in query.data:
        grp_id = query.message.chat.id
        i = query.data.split(":")[1]
        keyword = query.data.split(":")[2]
        reply_text, btn, alerts, fileid = await find_filter(grp_id, keyword)
        if alerts is not None:
            alerts = ast.literal_eval(alerts)
            alert = alerts[int(i)]
            alert = alert.replace("\\n", "\n").replace("\\t", "\t")
            await query.answer(alert,show_alert=True)



