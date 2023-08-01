import time
import random
from datetime import datetime, timedelta
from pyrogram import Client, filters
from pymongo import MongoClient
from Zebra import Zebra


# ------------------------------------------------------------------------------- #


BET_IMG = (
"https://telegra.ph/file/239392115af961581e0ba.jpg",
"https://telegra.ph/file/1559efe00e0403794fdf3.jpg",
"https://telegra.ph/file/5cac3685c2d2f49caaee0.jpg",
"https://telegra.ph/file/73682cb9146192f2797df.jpg",
"https://telegra.ph/file/b330fad543d88a31287b0.jpg",
"https://telegra.ph/file/ecf305a302f2a0535a4c4.jpg"
)

# ------------------------------------------------------------------------------- #

DATABASE_NAME = "MrsFallenBot"   
DATABASE_URL = "mongodb+srv://MrsFallenBot:MrsFallenBot@cluster0.hsedwn2.mongodb.net/?retryWrites=true&w=majority"

# ------------------------------------------------------------------------------- #

class Database:
    def __init__(self, url, name):
        self.client = MongoClient(url)
        self.db = self.client[name]
        self.user_collection = self.db['users']
    
    def insert_user(self, user_data):
        self.user_collection.insert_one(user_data)
    
    def update_user(self, user_id, update_data):
        self.user_collection.update_one({"user_id": user_id}, {"$set": update_data})
    
    def find_user(self, user_id):
        return self.user_collection.find_one({"user_id": user_id})
    
    def get_top_users(self, limit):
        return self.user_collection.find().sort("total_winnings", -1).limit(limit)
    
    def get_top_user(self):
        return self.user_collection.find().sort("total_winnings", -1).limit(1)[0]


database = Database(DATABASE_URL, DATABASE_NAME)

# ------------------------------------------------------------------------------- #

@Zebra.on_message(filters.command("rewards", prefixes=["/", "!"]))
def start_command_handler(client, message):
    user_id = message.from_user.id
    user = database.find_user(user_id)
    if user:
        client.send_photo(message.chat.id, photo=random.choice(BET_IMG), caption=f"**ʜᴇʟʟᴏ {message.from_user.first_name} ɢᴏᴛ ᴀʟʀᴇᴀᴅʏ ʀᴇᴡᴀᴅs.**")
        return

    user_data = {
        "user_id": user_id,
        "balance": 50000,
        "last_bonus_claimed": datetime.now(),
        "total_winnings": 0
    }
    database.insert_user(user_data)
    client.send_photo(message.chat.id, photo=random.choice(BET_IMG), caption=f"**ʜᴇʟʟᴏ {message.from_user.first_name} **\n\n**ʏᴏᴜʀ ɢᴇᴛ ʀᴇᴡᴀʀᴅ ɴᴏᴡ.**\n**ʏᴏᴜʀ ʙᴀʟᴀɴᴄᴇ ɪs '50,000' 💵**")


# ------------------------------------------------------------------------------- #

@Zebra.on_message(filters.command("bet", prefixes=["/", "!"]))
def bet_command_handler(client, message):
    user_id = message.from_user.id
    user = database.find_user(user_id)
    if not user:
        client.send_photo(message.chat.id, photo=random.choice(BET_IMG), caption=f"**ʜᴇʟʟᴏ {message.from_user.first_name}**\n\n**ʏᴏᴜ ʜᴀᴠᴇ ɴᴏᴛ ᴇɴᴏᴜɢʜ ʙᴀʟᴀɴᴄᴇ ᴘʟᴇᴀsᴇ ғɪʀsᴛs ɢᴇᴛ ʀᴇᴡᴀʀᴅs.** '/rewards'")
        return

    balance = user["balance"]

    try:
        bet_amount = int(message.command[1])
    except (ValueError, IndexError):
        client.send_photo(message.chat.id, photo=random.choice(BET_IMG), caption="**ᴘʟᴇᴀsᴇ sᴘᴇᴄɪғʏ ᴀ ᴠᴀʟɪᴅ ʙᴇᴛ ᴀᴍᴏᴜɴᴛ.**")
        return

    if balance < bet_amount:
        client.send_photo(message.chat.id, photo=random.choice(BET_IMG), caption=f"**ʜᴇʟʟᴏ {message.from_user.first_name} ɪɴsᴜғғɪᴄɪᴇɴᴛ ʙᴀʟᴀɴᴄᴇ.**")
        return
    random_number = random.randint(1, 10)

    if random_number <= 5:
        winnings = bet_amount * 2
        balance += winnings
        client.send_photo(message.chat.id, photo=random.choice(BET_IMG), caption=f"**ʜᴇʟʟᴏ {message.from_user.first_name}, ʏᴏᴜ ᴡᴏɴ !**\n\n**ʏᴏᴜʀ ᴡɪɴɴɪɴɢs**: {winnings} 💵\n**ᴛᴏᴛᴀʟ ʙᴀʟᴀɴᴄᴇ**: {balance} 💵")
    else:
        
        balance -= bet_amount
        client.send_photo(message.chat.id, photo=random.choice(BET_IMG), caption=f"**ʜᴇʟʟᴏ {message.from_user.first_name}, sᴏʀʀʏ**\n\n**ʏᴏᴜ ʟᴏsᴛ ᴛʜᴇ ʙᴇᴛ.**\n**ᴛᴏᴛᴀʟ ʙᴀʟᴀɴᴄᴇ**: {balance} 💵")

    database.update_user(
        user_id, {"balance": balance, "total_winnings": user["total_winnings"] + winnings}
    )
    

# ------------------------------------------------------------------------------- #


@Zebra.on_message(filters.command("bonus", prefixes=["/", "!"]))
def bonus_command_handler(client, message):
    user_id = message.from_user.id
    user = database.find_user(user_id)
    if not user:
        client.send_photo(message.chat.id, photo=random.choice(BET_IMG), caption=f"**ʜᴇʟʟᴏ {message.from_user.first_name}**\n\n**ʏᴏᴜ ʜᴀᴠᴇ ɴᴏᴛ ᴇɴᴏᴜɢʜ ʙᴀʟᴀɴᴄᴇ ᴘʟᴇᴀsᴇ ғɪʀsᴛs ɢᴇᴛ ʀᴇᴡᴀʀᴅs** '/rewards'")
        return

    balance = user["balance"]
    last_bonus_claimed = user["last_bonus_claimed"]

    if datetime.now() - last_bonus_claimed >= timedelta(weeks=1):
        balance += 10000
        last_bonus_claimed = datetime.now()
        client.send_photo(message.chat.id, photo=random.choice(BET_IMG), caption=f"**ʜᴇʟʟᴏ {message.from_user.first_name}**\n\n**ʏᴏᴜ ʀᴇᴄᴇɪᴠᴇᴅ ᴀ ᴡᴇᴇᴋʟʏ ʙᴏɴᴜs ᴏғ** '10,000' 💵\n**ɴᴇᴡ ʙᴀʟᴀɴᴄᴇ**: '{balance}' 💵")
    else:
        wait_time = (last_bonus_claimed + timedelta(weeks=1)) - datetime.now()
        client.send_photo(message.chat.id, photo=random.choice(BET_IMG), caption=f"**ʜᴇʟʟᴏ {message.from_user.first_name}**\n\nʏᴏᴜ ʜᴀᴠᴇ ᴀʟʀᴇᴀᴅ ᴄʟᴀɪᴍᴇᴅ ʏᴏᴜʀ ᴡᴇᴇᴋʟʏ ʙᴏɴᴜs**\n**ɴᴇxᴛ ʙᴏɴᴜs ᴀᴠᴀɪʟᴀʙʟᴇ ɪɴ {wait_time.days} ᴅᴀʏs.**")
    database.update_user(user_id, {"balance": balance, "last_bonus_claimed": last_bonus_claimed})


# ------------------------------------------------------------------------------- #

@Zebra.on_message(filters.command("leaderboards", prefixes=["/", "!"]))
def leaderboard_command_handler(client, message):
    top_10_users = database.get_top_users()

    leaderboard_message = "<b>ʙᴇᴛ ᴛᴏᴘ 10 ᴜsᴇʀs:</b>\n"
    rank = 1
    for user in top_10_users:
        user_info = client.get_chat_member(message.chat.id, user['user_id']).user
        user_first_name = user_info.first_name
        leaderboard_message += f"{rank}.| {user_first_name} » **ᴛᴏᴛᴀʟ ᴡɪɴɴɪɴɢs**: {user['total_winnings']} 💵\n"
        rank += 1
    client.send_photo(message.chat.id, photo=random.choice(BET_IMG), caption=leaderboard_message, parse_mode='html')


# ------------------------------------------------------------------------------- #

@Zebra.on_message(filters.command("topusers", prefixes=["/", "!"]))
def topuser_command_handler(client, message):
    top_user = database.get_top_user()
    user_info = client.get_chat_member(message.chat.id, top_user['user_id']).user
    user_first_name = user_info.first_name
    client.send_photo(message.chat.id, photo=random.choice(BET_IMG), caption=f"**ᴛʜᴇ ᴜsᴇʀ ᴡɪᴛʜ ʜɪɢʜᴇsᴛ ᴡɪɴɴɪɴɢs**\n\n**ᴡɪɴɴᴇʀ ɴᴀᴍᴇ**: {user_first_name}\n**ᴛᴏᴛᴀʟ ᴡɪɴɴɪɴɢs**: {top_user['total_winnings']} 💵")


# ------------------------------------------------------------------------------- #



