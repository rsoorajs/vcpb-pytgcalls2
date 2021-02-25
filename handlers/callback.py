from pyrogram import Client, filters
from pyrogram.types import CallbackQuery

from tgcalls import pytgcalls


@Client.on_callback_query(filters.regex("close"))
async def close(client: Client, query: CallbackQuery):
    await query.message.delete()


@Client.on_callback_query(filters.regex(".*raw"))
async def play_now(client: Client, query: CallbackQuery):
    file_path = query.data

    if query.message.chat.id in pytgcalls.get_active_voice_chats():
        pytgcalls.change_stream(query.message.chat.id, file_path)
    else:
        pytgcalls.join_group_call(query.message.chat.id, file_path)

    await query.message.edit_text("Playing...", reply_markup=None)
