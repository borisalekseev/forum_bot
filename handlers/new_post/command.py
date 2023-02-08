from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext

from config import dp
from states import NewPost
import messages


@dp.message_handler(Command("new_post"))
async def new_post(message: types.Message, state: FSMContext):
    await message.answer(messages.NEW_POST_TEXT)
    await NewPost.text.set()
