import asyncio
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from Hiroko import Hiroko
import time
import aiohttp
from asyncio import sleep
from pyrogram import filters, Client, enums
from pyrogram.enums import ParseMode
from pyrogram.types import Message





get_font = lambda font_size, font_path: ImageFont.truetype(font_path, font_size)
resize_text = (
    lambda text_size, text: (text[:text_size] + "...").upper()
    if len(text) > text_size
    else text.upper()
)


async def get_welcome_img(
    bg_path: str,
    font_path: str,
    user_id: int | str,
    name: str,
    username: str,
    chat_name: str,
    profile_path: str = None,
):
    bg = Image.open(bg_path)
    if profile_path:
        img = Image.open(profile_path)
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.pieslice([(0, 0), img.size], 0, 360, fill=255)

        circular_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
        circular_img.paste(img, (0, 0), mask)
        resized = circular_img.resize((440, 440))
        bg.paste(resized, (772, 140), resized)

    img_draw = ImageDraw.Draw(bg)

        
    img_draw.text(
        (890, 595),
        text=str(user_id).upper(),
        font=get_font(60, font_path),
        fill=(275, 275, 275),
    )

    img_draw.text(
        (180, 340),
        text=resize_text(60, name),
        font=get_font(100, font_path),
        fill=(275, 275, 275),
    )


    path = f"./Welcome_img_{user_id}.png"
    bg.save(path)
    return path


bg_path = "./Hiroko/Helper/assests/thumbnail.png"
font_path = "./Hiroko/Helper/assests/Hiroko.ttf"

  


# --------------------------------------------------------------------------------- #

INFO_TEXT = """
**ᴜsᴇʀ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ**:

**ᴜsᴇʀ ɪᴅ:** `{}`

**ɴᴀᴍᴇ:** {}
**ᴜsᴇʀɴᴀᴍᴇ: @{}
**ᴍᴇɴᴛɪᴏɴ:** {}

**ᴜsᴇʀ sᴛᴀᴛᴜs:**\n`{}`\n
**ᴅᴄ ɪᴅ:** {}
**ʙɪᴏ:** {}
"""

# --------------------------------------------------------------------------------- #

async def userstatus(user_id):
   try:
      user = await Hiroko.get_users(user_id)
      x = user.status
      if x == enums.UserStatus.RECENTLY:
         return "User was seen recently."
      elif x == enums.UserStatus.LAST_WEEK:
          return "User was seen last week."
      elif x == enums.UserStatus.LONG_AGO:
          return "User was seen long ago."
      elif x == enums.UserStatus.OFFLINE:
          return "User is offline."
      elif x == enums.UserStatus.ONLINE:
         return "User is online."
   except:
        return "**sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ʜᴀᴘᴘᴇɴᴇᴅ !**"
    

# --------------------------------------------------------------------------------- #

@Hiroko.on_message(filters.command(["pinfo", "puserinfo"]))
async def userinfo(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    if not message.reply_to_message and len(message.command) == 2:
        try:
            user_id = message.text.split(None, 1)[1]
            user_info = await Hiroko.get_chat(user_id)
            user = await Hiroko.get_users(user_id)
            status = await userstatus(user.id)
            id = user_info.id
            dc_id = user.dc_id
            name = user_info.first_name
            username = user_info.username
            mention = user.mention
            bio = user_info.bio
            photo = await Hiroko.download_media(user.photo.big_file_id)
            welcome_photo = await get_welcome_img(
                bg_path=bg_path,
                font_path=font_path,
                user_id=user_id,
                profile_path=photo,
            )
            await Hiroko.send_photo(chat_id, photo=welcome_photo, caption=INFO_TEXT.format(
                id, name, username, mention, status, dc_id, bio), reply_to_message_id=message.id)
        except Exception as e:
            await message.reply_text(str(e))
    
    elif not message.reply_to_message:
        try:
            user_info = await Hiroko.get_chat(user_id)
            user = await Hiroko.get_users(user_id)
            status = await userstatus(user.id)
            id = user_info.id
            dc_id = user.dc_id
            name = user_info.first_name
            username = user_info.username
            mention = user.mention
            bio = user_info.bio
            photo = await Hiroko.download_media(user.photo.big_file_id)
            welcome_photo = await get_welcome_img(
                bg_path=bg_path,
                font_path=font_path,
                user_id=user_id,
                profile_path=photo,
            )
            await Hiroko.send_photo(chat_id, photo=welcome_photo, caption=INFO_TEXT.format(
                id, name, username, mention, status, dc_id, bio), reply_to_message_id=message.id)
        except Exception as e:
            await message.reply_text(str(e))
    
    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        try:
            user_info = await Hiroko.get_chat(user_id)
            user = await Hiroko.get_users(user_id)
            status = await userstatus(user.id)
            id = user_info.id
            dc_id = user.dc_id
            name = user_info.first_name
            username = user_info.username
            mention = user.mention
            bio = user_info.bio
            photo = await Hiroko.download_media(message.reply_to_message.from_user.photo.big_file_id)
            welcome_photo = await get_welcome_img(
                bg_path=bg_path,
                font_path=font_path,
                user_id=user_id,
                profile_path=photo,
            )
            await Hiroko.send_photo(chat_id, photo=welcome_photo, caption=INFO_TEXT.format(
                id, name, username, mention, status, dc_id, bio), reply_to_message_id=message.id)
        except Exception as e:
            await message.reply_text(str(e))




