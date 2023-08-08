from Hiroko.Helper.database.rankingdb import get_name, increase_count, chatdb
from Hiroko import Hiroko
from pyrogram import filters
from datetime import date
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


@Hiroko.on_message(
    ~filters.bot
    & ~filters.forwarded
    & filters.group
    & ~filters.via_bot
    & ~filters.service
)
async def inc_user(_, message: Message):
    if message.text:
        if (
            message.text.strip() == "/rankings@HirokoRobot"
            or message.text.strip() == "/rankings"
        ):
            return await show_top_today(_, message)

    chat = message.chat.id
    user = message.from_user.id
    increase_count(chat, user)
    print(chat, user, "increased")


async def show_top_today(_, message: Message):
    print("today top in", message.chat.id)
    chat = chatdb.find_one({"chat": message.chat.id})
    today = str(date.today())

    if not chat:
        return await message.reply_photo(photo="https://telegra.ph//file/3f12d7ceb3aaa0eec6999.jpg",
                                         caption="**ɴᴏ ᴅᴀᴛᴀ ᴀᴠᴀɪʟᴀʙʟᴇ !**")

    if not chat.get(today):
        return await message.reply_photo(photo="https://telegra.ph//file/3f12d7ceb3aaa0eec6999.jpg",
                                         caption="**ɴᴏ ᴅᴀᴛᴀ ᴀᴠᴀɪʟᴀʙʟᴇ ғᴏʀ ᴛᴏᴅᴀʏ !**")

    t = "๏ **ᴛᴏᴅᴀʏ's ᴛᴏᴘ ʀᴀɴᴋɪɴɢs :**\n\n"

    pos = 1
    for i, k in sorted(chat[today].items(), key=lambda x: x[1], reverse=True)[:10]:
        i = await get_name(app, i)

        t += f"**{pos}.** {i} · {k}\n"
        pos += 1

    await message.reply_photo(
        photo="https://telegra.ph/file/55d2355063707105d71ca.jpg",
        caption=t,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("๏ ᴏᴠᴇʀᴀʟʟ ʀᴀɴᴋɪɴɢs ๏", callback_data="overall")]]
        ),
    )


@Hiroko.on_callback_query(filters.regex("overall"))
async def show_top_overall_callback(_, query: CallbackQuery):
    print("overall top in", query.message.chat.id)
    chat = chatdb.find_one({"chat": query.message.chat.id})

    if not chat:
        return await query.answer("**ɴᴏ ᴅᴀᴛᴀ ᴀᴠᴀɪʟᴀʙʟᴇ !**", show_alert=True)

    await query.answer("**ᴘʀᴏᴄᴇssɪɴɢ .... ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ**")

    t = "๏ **ᴏᴠᴇʀᴀʟʟ ᴛᴏᴘ ʀᴀɴᴋɪɴɢs :**\n\n"

    overall_dict = {}
    for i, k in chat.items():
        if i == "chat" or i == "_id":
            continue

        for j, l in k.items():
            if j not in overall_dict:
                overall_dict[j] = l
            else:
                overall_dict[j] += l

    pos = 1
    for i, k in sorted(overall_dict.items(), key=lambda x: x[1], reverse=True)[:10]:
        i = await get_name(app, i)

        t += f"**{pos}.** {i} · {k}\n"
        pos += 1

    await query.message.edit_text(
        t,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("๏ ᴛᴏᴅᴀʏ's ʀᴀɴᴋɪɴɢs ๏", callback_data="today")]]
        ),
    )


@Hiroko.on_callback_query(filters.regex("today"))
async def show_top_today_callback(_, query: CallbackQuery):
    print("today top in", query.message.chat.id)
    chat = chatdb.find_one({"chat": query.message.chat.id})
    today = str(date.today())

    if not chat:
        return await query.answer("**ɴᴏ ᴅᴀᴛᴀ ᴀᴠᴀɪʟᴀʙʟᴇ !**", show_alert=True)

    if not chat.get(today):
        return await query.answer("**ɴᴏ ᴅᴀᴛᴀ ᴀᴠᴀɪʟᴀʙʟᴇ ғᴏʀ ᴛᴏᴅᴀʏ !**", show_alert=True)

    await query.answer("**ᴘʀᴏᴄᴇssɪɴɢ .... ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ**")

    t = "๏ **ᴛᴏᴅᴀʏ's ᴛᴏᴘ ʀᴀɴᴋɪɴɢs :**\n\n"

    pos = 1
    for i, k in sorted(chat[today].items(), key=lambda x: x[1], reverse=True)[:10]:
        i = await get_name(app, i)

        t += f"**{pos}.** {i} · {k}\n"
        pos += 1

    await query.message.edit_text(
        t,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("๏ ᴏᴠᴇʀᴀʟʟ ʀᴀɴᴋɪɴɢs ๏", callback_data="overall")]]
        ),
    )




