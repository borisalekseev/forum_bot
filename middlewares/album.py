import asyncio

from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from aiogram import types


class AlbumMiddleware(BaseMiddleware):
    album = {}

    def __init__(self, latency: int | float = 0.01):
        self.latency = latency
        super().__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        if not message.media_group_id:
            return

        try:
            self.album[message.media_group_id].append(message)
            raise CancelHandler()
        except KeyError:
            self.album[message.media_group_id] = message.photo[-1].file_id
            await asyncio.sleep(self.latency)

            message.conf["is_last"] = True
            data["album"] = self.album[message.media_group_id]

    async def on_post_process_message(self, message: types.Message, result: dict, data: dict):
        if message.media_group_id and message.conf["is_last"]:
            del self.album[message.media_group_id]
