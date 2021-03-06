# Copyright (C) 2021 Veez Music-Project

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
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream import InputStream
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message


@Client.on_message(command(["stream", f"stream@{BOT_USERNAME}"]) & other_filters)
async def stream(_, message: Message):
    costumer = message.from_user.mention
    lel = await message.reply_text("**γ π²πΎπ½π½π΄π²ππΈπ½πΆ ππΎ π³π°ππΊ ππ΄πππ΄ππ γ**")

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="γ πππΏπΏπΎππ γ", url=f"https://t.me/{GROUP_SUPPORT}"
                ),
                InlineKeyboardButton(
                    text="γ π²π·π°π½π½π΄π» γ", url=f"https://t.me/{UPDATES_CHANNEL}"
                ),
            ]
        ]
    )

    audio = message.reply_to_message.audio if message.reply_to_message else None
    if not audio:
        return await lel.edit("π­ **please reply to a telegram audio file**")
    if round(audio.duration / 60) > DURATION_LIMIT:
        return await lel.edit(
            f"β **music with duration more than** `{DURATION_LIMIT}` **minutes, can't play !**"
        )

    title = audio.title
    file_name = get_file_name(audio)
    duration = convert_seconds(audio.duration)
    file_path = await converter.convert(
        (await message.reply_to_message.download(file_name))
        if not path.isfile(path.join("downloads", file_name))
        else file_name
    )
    chat_id = message.chat.id
    ACTV_CALLS = []
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))    
    if chat_id in ACTV_CALLS:
        position = await queues.put(chat_id, file=file_path)
        await message.reply_photo(
            photo=f"{QUE_IMG}",
            caption=f"π‘ **Track added to queue Β»** `{position}`\n\nπ· **Name:** {title[:50]}\nβ± **Duration:** `{duration}`\nπ§ **Request by:** {costumer}",
            reply_markup=keyboard,
        )
    else:
        await callsmusic.pytgcalls.join_group_call(
            chat_id, 
            InputStream(
                InputAudioStream(
                    file_path,
                ),
            ),
        )
        await message.reply_photo(
            photo=f"{ALIVE_IMG}",
            caption=f"βͺ **π½π°πΌπ΄:** {title[:50]}\nβͺ **π³πππ°ππΈπΎπ½:** `{duration}`\nβͺ **πππ°πππ:** `πΏπ»π°ππΈπ½πΆ`\n"
            + f"βͺ**ππ΄πππ΄ππ π±π:** {costumer}",
            reply_markup=keyboard,
        )

    return await lel.delete() 
