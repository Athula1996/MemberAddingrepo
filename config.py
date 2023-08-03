import os
from os import getenv


API_ID = int(getenv("API_ID", "26850449"))
API_HASH = getenv("API_HASH", "72a730c380e68095a8549ad7341b0608")
BOT_USERNAME = getenv("BOT_USERNAME", "HirokoRobot")
COMMAND_HANDLER = ["/", "!"]
BOT_TOKEN = getenv("BOT_TOKEN", "6552685718:AAFNWz5Rk7CBeqLYT2c2ty868wW280ygm7o")
OWNER_ID = int(getenv("OWNER_ID", "6109551937"))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "6109551937 5416887843 5896960462").split()))
MONGO_URL = getenv("MONGO_URI", "mongodb+srv://MrsFallenBot:MrsFallenBot@cluster0.hsedwn2.mongodb.net/?retryWrites=true&w=majority")
