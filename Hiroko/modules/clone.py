from pymongo import MongoClient
from config import MONGO_URL
from Hiroko import Hiroko
from pyrogram import filters, Client 
from pyrogram.types import Message 



def create_database():

    client = MongoClient(MONGO_URL)    
    db = client['bots']   
    collection = db['tokens']   
    return collection

def add_token(token):
    collection = create_database()    
    collection.insert_one({'token': token})


def retrieve_tokens():
    collection = create_database()    
    tokens = list(collection.find({}, {'_id': 0}))    
    return tokens


def delete_token(token):
    collection = create_database()    
    collection.delete_one({'token': token})



@Hiroko.on_message(filters.private & filters.command("clone"))
async def clone(bot, msg: Message):
    chat = msg.chat
    text = await msg.reply("Usage:\n\n /clone token")
    cmd = msg.command
    token = msg.command[1]
    
    try:
        await text.edit("Booting Your Client")
        client = Client(":memory:", API_ID, API_HASH, bot_token=token, plugins={"root": "Hiroko.modules"})
        await client.start()
        user = await client.get_me()
        
        add_token(token)
        
        await msg.reply(f"Your Client Has Been Successfully Started As @{user.username}! ✅ \n\n Now Add Your Bot!\n\nThanks for Cloning.")
    
    except Exception as e:
        await msg.reply(f"**ERROR:** `{str(e)}`\nPress /start to Start again.")


@Hiroko.on_message(filters.private & filters.command("del"))
async def delete_token(bot, msg: Message):
    chat = msg.chat
    text = await msg.reply("Usage:\n\n /del token")
    cmd = msg.command
    token = msg.command[1]
    
    try:
        # Delete the bot token from the MongoDB database
        delete_token(token)
        
        await text.edit(f"Bot token {token} has been deleted.")
    
    except Exception as e:
        await msg.reply(f"**ERROR:** `{str(e)}`\nPress /start to Start again.")




