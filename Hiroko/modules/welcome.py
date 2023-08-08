import asyncio
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from pyrogram import Client, filters
from Hiroko import Hiroko


bg_path = "./Hiroko/Helper/assests/thumbnail.png"
font_path = "./Hiroko/Helper/assests/Hiroko.ttf"
WELCOME_TEXT = """
ᴡᴇʟᴄᴏᴍᴇ {name}

ᴛʜᴀɴᴋs ғᴏʀ ᴊᴏɪɴɪɴɢ ᴏᴜʀ **{chat_title}** !
"""
DEL_AFTER_WELCOME = True

async def get_welcome_img(bg_path: str, font_path: str, user_id: int | str, name: str, username: str, chat_name: str, profile_path: str = None):
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
        text=resize_text(60, chat_name),
        font=get_font(100, font_path),
        fill=(275, 275, 275),
    )

    path = f"./Welcome_img_{user_id}.png"
    bg.save(path)
    return path




async def download_profile_photo(client, photo_id):
    try:
        profile = await client.download_media(photo_id)
    except AttributeError:
        profile = None
    return profile


@Hiroko.on_message(filters.new_chat_members, group=3)
async def greet_users(client, message):
    chat = message.chat
    my_id = client.me.id
    tasks = []
    
    for member in message.new_chat_members:
        user_id = member.id
        username = member.username
        name = member.first_name if member.first_name else member.last_name
        if user_id == my_id:
            continue
        
        tasks.append(download_profile_photo(client, member.photo.big_file_id))
    
    profile_paths = await asyncio.gather(*tasks)
    
    for member, profile_path in zip(message.new_chat_members, profile_paths):
        user_id = member.id
        username = member.username
        name = member.first_name if member.first_name else member.last_name
        welcome_photo = await get_welcome_img(
            bg_path=bg_path,
            font_path=font_path,
            user_id=user_id,
            name=name,
            username=username,
            chat_name=chat.title,
            profile_path=profile_path,
        )
        welcome_caption = WELCOME_TEXT.format(
            chat_title=chat.title, name=name, username=username, user_id=user_id
        )
        async with await Hiroko.send_photo(
            chat_id=chat.id, photo=welcome_photo, caption=welcome_caption
        ) as msg:
            if DEL_AFTER_WELCOME:
                async def del_welcome_pic():
                    await asyncio.sleep(10 * 60)
                    await msg.delete()

                loop = asyncio.get_running_loop()
                loop.create_task(del_welcome_pic())

        Path(welcome_photo).unlink(missing_ok=True)


