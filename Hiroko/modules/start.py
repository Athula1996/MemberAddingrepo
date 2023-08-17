import asyncio
import random
from time import time
from datetime import datetime
from config import BOT_USERNAME, OWNER_ID
from pyrogram import filters, Client
from Hiroko import Hiroko
from pyrogram.enums import ChatType
from pyrogram.errors import MessageNotModified
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

# ------------------------------------------------------------------------------- #

START_IMG = (
"https://telegra.ph/file/c4ca1a162f89bdb5b6671.jpg",
"https://telegra.ph/file/d5f41e8fe3c734431d6f1.jpg",
"https://telegra.ph/file/f37357df411a6f546fe69.jpg",
"https://telegra.ph/file/3c82d2ebe9f7c50292acc.jpg"
)



# ------------------------------------------------------------------------------- #

START_TEXT = """
**ʜᴇʏ ᴛʜᴇʀᴇ [{}](tg://user?id={}) ɴɪᴄᴇ ᴛᴏ ᴍᴇᴇᴛ ʏᴏᴜ !**
━━━━━━━━━━━━━━━━━━━━━━**
๏ ɪ ᴀᴍ ˹ʜɪꝛᴏᴋᴏ ꝛᴏʙᴏᴛ˼ ᴀɴᴅ ɪ ʜᴀᴠᴇ sᴘᴇᴄɪᴀʟ ғᴇᴀᴛᴜʀᴇs
๏ ɪ ᴀᴍ ᴅɪғғᴇʀᴇɴᴛ ғʀᴏᴍ ᴀɴᴏᴛʜᴇʀ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛs

๏ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʜᴇʟᴩ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴍʏ ᴍᴏᴅᴜʟᴇs ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅs**
"""


# ------------------------------------------------------------------------------- #

@Hiroko.on_message(filters.command(["start"], prefixes=["/", "!"]))
async def start(client: Client, message: Message):    
        get_me = await client.get_me()
        BOT_USERNAME = get_me.username
        buttons = [
            [
                InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
            ],
            [
                InlineKeyboardButton("✨ sᴜᴘᴘᴏʀᴛ ✨", url="https://t.me/TheNixaSupport"),
                InlineKeyboardButton("🎓 ᴍᴀɪɴᴛᴀɪɴᴇʀ", url=f"https://t.me/AnonDeveloper"),
            ],
                
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(START_IMG),
            caption=START_TEXT.format(message.from_user.first_name, message.from_user.id),
            reply_markup=reply_markup
        )
        
          

# ------------------------------------------------------------------------------- #


