from os import path

import converter
from callsmusic import callsmusic, queues
from config import (
    AUD_IMG,
    BOT_USERNAME,
    DURATION_LIMIT,
    GROUP_SUPPORT,
    QUE_IMG,
    UPDATES_CHANNEL,
)
from handlers.play import convert_seconds
from helpers.filters import command, other_filters
from helpers.gets import get_file_name
from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message


@Client.on_message(command(["stream", f"stream@{BOT_USERNAME}"]) & other_filters)
async def stream(_, message: Message):

    lel = await message.reply("🔁 **معالجة** صوت...")
    costumer = message.from_user.mention

    keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="🏆︙ جيت هاب نينجا",
                        url=f"https://t.me/{GROUP_SUPPORT}"),
                    InlineKeyboardButton(
                        text="🖤︙ - RoLeS ›",
                        url=f"https://t.me/{UPDATES_CHANNEL}")
                ]
            ]
        )

    audio = message.reply_to_message.audio if message.reply_to_message else None

    if not audio:
        return await lel.edit("🗼 **الرجاء الرد على ملف صوتي برقية**")
    if round(audio.duration / 60) > DURATION_LIMIT:
        return await lel.edit(f"❌ **الموسيقى مع مدة أكثر من** `{DURATION_LIMIT}` **دقائق، لا يمكن أن تلعب !**")

    # tede_ganteng = True
    file_name = get_file_name(audio)
    title = audio.title
    duration = convert_seconds(audio.duration)
    file_path = await converter.convert(
        (await message.reply_to_message.download(file_name))
        if not path.isfile(path.join("downloads", file_name)) else file_name
    )
    # ambil aja bg
    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
            photo=f"{QUE_IMG}",
            caption=f"🗼 **تعقب تمت إضافته إلى قائمة الانتظار »** `{position}`\n\n🎸 **اسم:** {title[:50]}\n🗼 **دقاق:** `{duration}`\n🦹🏻 **طلب من قبل:** {costumer}",
            reply_markup=keyboard,
        )
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        await message.reply_photo(
            photo=f"{AUD_IMG}",
             caption=f"🖤 **Track added to the queue**\n\n🖤 **name :** [{title[:35]}]({url})\n⏱ **Duration:** `{duration}`\n🔮 **wanted by me :** {message.from_user.mention}\n" \
                   +f"🔢 **At Position:** » `{position}` «",
            reply_markup=keyboard
        )

    return await lel.delete()
