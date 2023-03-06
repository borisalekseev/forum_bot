import asyncio

import aiogram
from aiogram import executor

from handlers import dp
from config import ACCESS_ID_LIST
from middlewares import AlbumMiddleware, AccessMiddleware
from jobs import on_shutdown_tasks, on_start_tasks, check_new_posts

from database.initialize import init


async def on_startup(dispatcher: aiogram.Dispatcher):
    await init()
    dispatcher.setup_middleware(AlbumMiddleware())
    dispatcher.setup_middleware(AccessMiddleware(ACCESS_ID_LIST))
    loop = asyncio.get_event_loop()
    loop.create_task(check_new_posts())
    await on_start_tasks()


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown_tasks)
