import asyncio

from aiogram import types
from aiogram.dispatcher.filters import CommandStart, AdminFilter

from config import dp
import messages


@dp.message_handler(CommandStart())
async def start(message: types.Message):
    await asyncio.sleep(5)
    await message.answer(messages.START.format(message.from_user.full_name))
