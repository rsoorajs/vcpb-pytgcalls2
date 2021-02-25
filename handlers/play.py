from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from tgcalls import pytgcalls
from converter import convert
from youtube import download
from helpers.wrappers import errors


@Client.on_message(
    filters.command("play")
    & filters.group
    & ~ filters.edited
)
@errors
async def play(client: Client, message_: Message):
    messages = [message_]
    text = ""
    offset = None
    length = None

    if message_.reply_to_message:
        messages.append(message_.reply_to_message)

    for message in messages:
        if offset:
            break

        if message.entities:
            for entity in message.entities:
                if entity.type == "url":
                    text = message.text or message.caption
                    offset, length = entity.offset, entity.length
                    break

    if offset == None:
        await message_.reply_text("You did not provide a video URL.")
        return

    url = text[offset:offset+length]

    await message_.reply_text("Downloading and converting...")

    file_path = await convert(download(url))

    if message_.chat.id in pytgcalls.get_active_voice_chats():
        await message_.reply_text(
            "There is a song being played at the moment, what do you want to do?",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Play now", callback_data=file_path
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "Don't play, close this.", callback_data="close"
                        )
                    ]
                ]
            )
        )
    else:
        await message_.reply_text("Playing...")
        pytgcalls.join_group_call(message_.chat.id, file_path, 48000)
