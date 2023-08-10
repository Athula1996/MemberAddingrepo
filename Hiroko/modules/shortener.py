import aiohttp
import motor.motor_asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, ChatMemberUpdated
from Hiroko import Hiroko as Shortener


DATABASE_URL = "mongodb+srv://MrsFallenBot:MrsFallenBot@cluster0.hsedwn2.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "MrsFallenBot"


import logging
logging.basicConfig(level=logging.INFO)

# -----------------» ᴍᴏɴɢᴏ-ᴅᴀᴛʙᴀsᴇ «----------------- #

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.user
    
    async def add_user(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)
    
    def new_user(self, id):
        return {"_id": id, "api_key": None, "api_url": None}
    
    async def set_api_data(self, user_id, api_key, api_url):
        await self.col.update_one({"_id": user_id}, {"$set": {"api_key": api_key, "api_url": api_url}}, upsert=True)
    
    async def get_api_data(self, user_id):
        user_data = await self.col.find_one({"_id": user_id})
        if user_data and "api_key" in user_data and "api_url" in user_data:
            return user_data["api_key"], user_data["api_url"]
        else:
            return None, None

mongo = Database(DATABASE_URL, DATABASE_NAME)



# -----------------» sʜᴏʀᴛɴᴇʀ-ᴅᴀᴛʙᴀsᴇ «----------------- #

@Shortener.on_message(filters.command("shortener"))
async def set_api_handler(client, message):
    try:
        _, api_key, api_url = message.text.split(" ")
    except ValueError:
        await message.reply_text("<b>» ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀɴ ᴀᴘɪ_ᴋᴇʏ ᴀɴᴅ ᴀᴘɪ_ᴜʀʟ !\n\nғᴏʀᴍᴀᴛ: <code>/shortener api_key api_url</code></b>")
        return

    try:
        await mongo.set_api_data(message.from_user.id, api_key, api_url)
        await message.reply_text(f"<b>sᴜᴄᴄᴇssғᴜʟʟʏ sᴇᴛ sʜᴏʀᴛʟɪɴᴋ ᴀᴘɪ ғᴏʀ ʏᴏᴜʀ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ.\n\nᴄᴜʀʀᴇɴɢ sʜᴏʀᴛʟɪɴᴋ ᴡᴇʙsɪᴛᴇ: <code>{api_url}</code>\nᴄᴜʀʀᴇɴᴛ ᴀᴘɪ: <code>{api_key}</code></b>")
    except Exception as e:
        logging.error(f"<b>ᴇʀʀᴏʀ sᴇᴛᴛɪɴɢ ᴀᴘɪ ᴅᴀᴛᴀ ғᴏʀ ᴜsᴇʀ</b> {message.from_user.id}: {e}")
        await message.reply_text("<b>ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ sᴇᴛᴛɪɴɢ ᴛʜᴇ ᴀᴘɪ ᴅᴀᴛᴀ. ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.</b>")


# -----------------» ʟɪɴᴋ-ɢᴇɴᴇʀᴀᴛᴇ «----------------- #

@Shortener.on_message(filters.regex(r'https?://[^\s]+') & filters.private)
async def link_handler(client, message):
    api_key, api_url = await mongo.get_api_data(message.from_user.id)
    if not api_key or not api_url:
        await message.reply_text("» ᴘʟᴇᴀsᴇ sᴇᴛ ʏᴏᴜ ᴀᴘɪ_ᴋᴇʏ ᴀɴᴅ ᴀᴘɪ_ᴜʀʟ ғɪʀsᴛ ᴜsɪɴɢ /shortener ᴄᴏᴍᴍᴀɴᴅ !")
        return

    link = message.matches[0].group(0)
    try:
        short_link = await get_shortlink(link, api_key, api_url)
        await message.reply_text(f"☉ ʜᴇʀᴇ's ʏᴏᴜʀ sʜᴏʀᴛᴇɴᴇᴅ ʟɪɴᴋ:\n\n☉ {short_link}", quote=True)
    except Exception as e:
        logging.error(f"<b>ᴇʀʀᴏʀ sʜᴏʀᴛᴇɴɪɴɢ ʟɪɴᴋ ғᴏʀ ᴜsᴇʀ</b> {message.from_user.id}: {e}")
        await message.reply_text(f"<b>sᴏʀʀʏ, ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ sʜᴏʀᴛᴇɴɪɴɢ ᴛʜᴇ ʟɪɴᴋ:</b> {e}", quote=True)


async def get_shortlink(link, api_key, api_url):    
    params = {'api': api_key, 'url': link}
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url, params=params, raise_for_status=True) as response:
            data = await response.json()
            return data["shortenedUrl"]
