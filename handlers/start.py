import asyncio

from aiogram import types
from aiogram.dispatcher.filters import Command

from config import dp
import messages


@dp.message_handler(Command("start"))
async def start(message: types.Message):
    await message.answer(messages.START.format(message.from_user.full_name))
