from YourBot import pgram
from pyrogram import filters
import pyrogram
from uuid import uuid4
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup

@pgram.on_message(filters.command("packkang"))
async def _packkang(app,message):
    '''
    @MaybeSuraj on telegram. who helped me in making this module.
    '''
    txt = await message.reply_text("ᴘʀᴏᴄᴇssɪɴɢ....")
    if not message.reply_to_message:
        await txt.edit('ʀᴇᴘʟʏ ᴛᴏ ᴍᴇssᴀɢᴇ')
        return
    if not message.reply_to_message.sticker:
        await txt.edit('ʀᴇᴘʟʏ ᴛᴏ sᴛɪᴄᴋᴇʀ')
        return
    if message.reply_to_message.sticker.is_animated or  message.reply_to_message.sticker.is_video:
        return await txt.edit("ʀᴇᴘʟʏ ᴛᴏ ᴀ ɴᴏɴ-ᴀɴɪᴍᴀᴛᴇᴅ sᴛɪᴄᴋᴇʀ")
    if len(message.command) < 2:
        pack_name =  f'{message.from_user.first_name}_sticker_pack_by_@Yor_Robot'
    else :
        pack_name = message.text.split(maxsplit=1)[1]
    short_name = message.reply_to_message.sticker.set_name
    stickers = await app.invoke(
        pyrogram.raw.functions.messages.GetStickerSet(
            stickerset=pyrogram.raw.types.InputStickerSetShortName(
                short_name=short_name),
            hash=0))
    shits = stickers.documents
    sticks = []
    
    for i in shits:
        sex = pyrogram.raw.types.InputDocument(
                id=i.id,
                access_hash=i.access_hash,
                file_reference=i.thumbs[0].bytes
            )
        
        sticks.append(
            pyrogram.raw.types.InputStickerSetItem(
                document=sex,
                emoji=i.attributes[1].alt
            )
        )

    try:
        short_name = f'stikcer_pack_{str(uuid4()).replace("-","")}_by_{app.me.username}'
        user_id = await app.resolve_peer(message.from_user.id)
        await app.invoke(
            pyrogram.raw.functions.stickers.CreateStickerSet(
                user_id=user_id,
                title=pack_name,
                short_name=short_name,
                stickers=sticks,
            )
        )
        await txt.edit(f"𝙿𝙰𝙲𝙺 [𝙺𝙰𝙽𝙶𝙴𝙳](http://t.me/addstickers/{short_name})!\n𝚃𝙾𝚃𝙰𝙻 𝚂𝚃𝙸𝙲𝙺𝙴𝚁: {len(sticks)}",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ᴘᴀᴄᴋ ʟɪɴᴋ",url=f"http://t.me/addstickers/{short_name}")]]))
    except Exception as e:
        await message.reply(str(e))
