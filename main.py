import asyncio

import aiogram
from aiogram import executor

from handlers import dp
from config import ACCESS_ID_LIST
from middlewares import AlbumMiddleware, AccessMiddleware


async def on_startup(dispatcher: aiogram.Dispatcher):
    dispatcher.setup_middleware(AlbumMiddleware())
    dispatcher.setup_middleware(AccessMiddleware(ACCESS_ID_LIST))


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
