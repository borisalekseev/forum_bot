from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from aiogram import types

import messages


class AccessMiddleware(BaseMiddleware):
    def __init__(self, access_list: list[str]):
        self.access_list = access_list
        super().__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        if str(message.from_user.id) not in self.access_list:
            await message.answer(messages.ACCESS_DENIED + str(message.from_user.id))
            raise CancelHandler()
