from pyrogram import Client
from pytgcalls import PyTgCalls

import config


client = Client(config.SESSION_NAME, config.API_ID, config.API_HASH)
pytgcalls = PyTgCalls(1512, False)


@pytgcalls.on_stream_end()
def on_stream_end(chat_id: int) -> None:
    pytgcalls.leave_group_call(chat_id)


def run():
    pytgcalls.run(client)
