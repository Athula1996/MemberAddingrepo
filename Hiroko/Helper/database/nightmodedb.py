from pymongo.mongo_client import MongoClient
from typing import Dict, List, Union

uri = "mongodb+srv://public:abishnoimf@cluster0.rqk6ihd.mongodb.net/?retryWrites=true&w=majority"
mongo = MongoClient(uri).Rankings
nightdb = mongo.nightmode


async def nightmode_on(chat_id : int) :
    return nightdb.insert_one({"chat_id" : chat_id})     
    
async def nightmode_off(chat_id : int):
    return nightdb.delete_one({"chat_id" : chat_id})

async def get_nightchats() -> list:
    chats = nightdb.find({"chat_id": {"$lt": 0}})
    if not chats:
        return []
    chats_list = []
    for chat in await chats.to_list(length=1000000000):
        chats_list.append(chat)
    return chats_list
