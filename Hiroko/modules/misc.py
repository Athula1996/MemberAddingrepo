import time
import aiohttp
import wikipedia
from asyncio import sleep
from Hiroko import Hiroko
from pyrogram import filters, Client, enums
from pyrogram.enums import ParseMode
from pyrogram.types import Message




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


@Hiroko.on_message(filters.command(["info","userinfo"]))
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
            await Hiroko.send_photo(chat_id,photo=photo, caption=INFO_TEXT.format(
id,name, username, mention, status, dc_id, bio),reply_to_message_id=message.id)
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
            await Hiroko.send_photo(chat_id,photo=photo, caption=INFO_TEXT.format(
id,name, username, mention,status, dc_id, bio),reply_to_message_id=message.id)
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
            await Hiroko.send_photo(chat_id,photo=photo,caption=INFO_TEXT.format(
id,name, username, mention,status, dc_id, bio),reply_to_message_id=message.id)
          except Exception as e:
              await message.reply_text(str(e))


# --------------------------------------------------------------------------------- #

@Hiroko.on_message(filters.command('id'))
async def getid(client, message):
    chat = message.chat
    your_id = message.from_user.id
    message_id = message.id
    reply = message.reply_to_message

    text = f"**[ᴍᴇssᴀɢᴇ ɪᴅ:]({message.link})** `{message_id}`\n"
    text += f"**[ʏᴏᴜʀ ɪᴅ:](tg://user?id={your_id})** `{your_id}`\n"

    if not message.command:
        message.command = message.text.split()

    if not message.command:
        message.command = message.text.split()

    if len(message.command) == 2:
        try:
            split = message.text.split(None, 1)[1].strip()
            user_id = (await client.get_users(split)).id
            text += f"**[ᴜsᴇʀ ɪᴅ:](tg://user?id={user_id})** `{user_id}`\n"

        except Exception:
            return await message.reply_text("ᴛʜɪs ᴜsᴇʀ ᴅᴏᴇsɴ'ᴛ ᴇxɪsᴛ.", quote=True)

    text += f"**[ᴄʜᴀᴛ ɪᴅ:](https://t.me/{chat.username})** `{chat.id}`\n\n"

    if (
        not getattr(reply, "empty", True)
        and not message.forward_from_chat
        and not reply.sender_chat
    ):
        text += f"**[ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ ɪᴅ:]({reply.link})** `{reply.id}`\n"
        text += f"**[ʀᴇᴘʟɪᴇᴅ ᴜsᴇʀ ɪᴅ:](tg://user?id={reply.from_user.id})** `{reply.from_user.id}`\n\n"

    if reply and reply.forward_from_chat:
        text += f"ᴛʜᴇ ғᴏʀᴡᴀʀᴅᴇᴅ ᴄʜᴀɴɴᴇʟ, {reply.forward_from_chat.title}, ʜᴀs ᴀɴ ɪᴅ ᴏғ `{reply.forward_from_chat.id}`\n\n"
        print(reply.forward_from_chat)

    if reply and reply.sender_chat:
        text += f"ɪᴅ ᴏғ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴄʜᴀᴛ/ᴄʜᴀɴɴᴇʟ, ɪs `{reply.sender_chat.id}`"
        print(reply.sender_chat)

    await message.reply_text(
        text,
        disable_web_page_preview=True,
        parse_mode=ParseMode.DEFAULT,
    )


# --------------------------------------------------------------------------------- #

@Hiroko.on_message(filters.command(["github", "git"]))
async def github(_, message):
    if len(message.command) != 2:
        await message.reply_text("/git Sumit0045")
        return
    username = message.text.split(None, 1)[1]
    URL = f'https://api.github.com/users/{username}'
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as request:
            if request.status == 404:
                return await message.reply_text("404")

            result = await request.json()
            try:
                url = result['html_url']
                name = result['name']
                company = result['company']
                bio = result['bio']
                created_at = result['created_at']
                avatar_url = result['avatar_url']
                blog = result['blog']
                location = result['location']
                repositories = result['public_repos']
                followers = result['followers']
                following = result['following']
                caption = f"""**ɢɪᴛʜᴜʙ ɪɴғᴏ ᴏғ {name}**

**ᴜsᴇʀɴᴀᴍᴇ :** `{username}`
**ʙɪᴏ :** `{bio}`
**ʟɪɴᴋ :** [Here]({url})
**ᴄᴏᴍᴩᴀɴʏ :** `{company}`
**ᴄʀᴇᴀᴛᴇᴅ ᴏɴ :** `{created_at}`
**ʀᴇᴩᴏsɪᴛᴏʀɪᴇs :** `{repositories}`
**ʙʟᴏɢ :** `{blog}`
**ʟᴏᴄᴀᴛɪᴏɴ :** `{location}`
**ғᴏʟʟᴏᴡᴇʀs :** `{followers}`
**ғᴏʟʟᴏᴡɪɴɢ :** `{following}`"""
            except Exception as e:
                print(str(e))
                pass
    await message.reply_photo(photo=avatar_url, caption=caption)

# --------------------------------------------------------------------------------- #

@Hiroko.on_message(filters.command(["instatus","instat"]))
async def instatus(c: Hiroko, m: Message):
    start_time = time.perf_counter()
    user = await c.get_chat_member(m.chat.id, m.from_user.id)
    count = await c.get_chat_members_count(m.chat.id)
    if user.status in (
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ):
        sent_message = await m.reply_text("**ɪs ɢᴀᴛʜᴇʀɪɴɢ ᴜsᴇʀ ɪɴғᴏʀᴍᴀᴛɪᴏɴ...**")
        recently = 0
        within_week = 0
        within_month = 0
        long_time_ago = 0
        deleted_acc = 0
        premium_acc = 0
        no_username = 0
        restricted = 0
        banned = 0
        uncached = 0
        bot = 0
        async for ban in c.get_chat_members(
            m.chat.id, filter=enums.ChatMembersFilter.BANNED
        ):
            banned += 1
        async for restr in c.get_chat_members(
            m.chat.id, filter=enums.ChatMembersFilter.RESTRICTED
        ):
            restricted += 1
        async for member in c.get_chat_members(m.chat.id):
            user = member.user
            if user.is_deleted:
                deleted_acc += 1
            elif user.is_bot:
                bot += 1
            elif user.is_premium:
                premium_acc += 1
            elif not user.username:
                no_username += 1
            elif user.status.value == "recently":
                recently += 1
            elif user.status.value == "last_week":
                within_week += 1
            elif user.status.value == "last_month":
                within_month += 1
            elif user.status.value == "long_ago":
                long_time_ago += 1
            else:
                uncached += 1
        end_time = time.perf_counter()
        timelog = "{:.2f}".format(end_time - start_time)
        await sent_message.edit(
            "<b>💠 {}\n👥 {} ᴍᴇᴍʙᴇʀ\n——————\n👁‍🗨ᴍᴇᴍʙᴇʀ sᴛᴀᴛᴜs ɪɴғᴏʀᴍᴀᴛɪᴏɴ \n——————\n</b>🕒 <code>ʀᴇᴄᴇɴᴛʟʏ</code>: {}\n🕒 <code>ʟᴀsᴛ_ᴡᴇᴇᴋ</code>: {}\n🕒 <code>ʟᴀsᴛ_ᴍᴏɴᴛʜ</code>: {}\n🕒 <code>ʟᴏɴɢ_ᴀɢᴏ</code>: {}\n🔎 ɴᴏ ᴜsᴇʀɴᴀᴍᴇ: {}\n🤐 ʀᴇsᴛʀɪᴄᴛᴇᴅ: {}\n🚫 ʙʟᴏᴄᴋᴇᴅ: {}\n👻 ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛ (<code>/zombies</code>): {}\n🤖 ʙᴏᴛ: {}\n⭐️ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀ: {}\n👽 ᴜɴᴄᴀᴄʜᴇᴅ: {}\n\n⏱ ᴇxᴇᴄᴜᴛɪᴏɴ ᴛɪᴍᴇ {} sᴇᴄᴏɴᴅ.".format(
                m.chat.title,
                count,
                recently,
                within_week,
                within_month,
                long_time_ago,
                no_username,
                restricted,
                banned,
                deleted_acc,
                bot,
                premium_acc,
                uncached,
                timelog,
            )
        )
    else:
        sent_message = await m.reply_text(
            "❗ **ʏᴏᴜ ᴍᴜsᴛ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴏʀ ɢʀᴏᴜᴘ ᴏᴡɴᴇʀ ᴛᴏ ᴘᴇʀғᴏʀᴍ ᴛʜɪs ᴀᴄᴛɪᴏɴ.**"
        )
        await sleep(5)
        await sent_message.delete()

# --------------------------------------------------------------------------------- #


@Hiroko.on_message(filters.command("math", prefixes="/"))
def calculate_math(client, message):   
    expression = message.text.split("/math ", 1)[1]
    try:        
        result = eval(expression)
        response = f"The result is: {result}"
    except:
        response = "Invalid expression"
    message.reply(response)


# ------------------------------------------------------------------------------- #

@Hiroko.on_message(filters.command("wiki"))
async def wikipediasearch(_, message):
    reply = message.reply_to_message
    if len(message.command) < 2:
          await message.reply_text("**ᴇxᴀᴍᴘʟᴇ**:\n`/wiki telegram`")
          return 
    query = (
        message.text.split(None, 1)[1]
        if len(message.command) < 3
        else message.text.split(None, 1)[1].replace(" ", "%20")
    )
    if not query:
        await message.reply_text("**ɪɴᴠᴀʟɪᴅ sʏɴᴛᴀx sᴇᴇ ʜᴇʟᴘ ᴍᴇɴᴜ ᴛᴏ ᴋɴᴏᴡ ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.**")
        return
    msg = await message.reply_text("**sᴇᴀʀᴄʜɪɴɢ...**")
    results = wikipedia.search(query)
    result = ""
    for s in results:
        try:
            page = wikipedia.page(s)
            url = page.url
            result += f"𒊹︎︎︎[{s}]({url}) \n"
        except BaseException:
            pass
    await message.reply_text(
        "**ᴡɪᴋɪᴘᴇᴅɪᴀ sᴇᴀʀᴄʜ: {}** \n\n**ʀᴇsᴜʟᴛ:**\n{}".format(query, result), disable_web_page_preview=True)
    await msg.delete()


# ------------------------------------------------------------------------------- #



