from pyrogram import Client, filters
import requests
from pyrogram.types import Message
from Hiroko import Hiroko


async def get_logo(name : str,message  : Message):

        API = f"https://api.princexd.tech/logo?text={name}"
        r = requests.get(API)
        if r.status_code == 200:
            return r.json()['url']
        else :
            return await message.reply("Api is Down.Can't Proceed your request")


@Hiroko.on_message(filters.command('logo'))
async def _logo(client,message):
     if len(message.command) == 1:
          return await message.reply("Please provide some text.")
     name = message.text.split(maxsplit=1)[1]
     logo = await get_logo(name,message)
     return await message.reply_photo(logo,caption="Logo created by Hiroko Robot")
        




