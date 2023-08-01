import os
from os import getenv


API_ID = int(getenv("API_ID", "26850449"))
API_HASH = getenv("API_HASH", "72a730c380e68095a8549ad7341b0608")
BOT_USERNAME = getenv("BOT_USERNAME", "@ZebraXRobot")
COMMAND_HANDLER = ["/", "!"]
BOT_TOKEN = getenv("BOT_TOKEN", "5693927648:AAHIQl8S4_gSDWUoSyha6APjVs7Bnm7PgPk")
OWNER_ID = int(getenv("OWNER_ID", "6109551937"))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "6109551937 5416887843").split()))
MONGO_URL = getenv("MONGO_URI", "mongodb+srv://MrsFallenBot:MrsFallenBot@cluster0.hsedwn2.mongodb.net/?retryWrites=true&w=majority")
