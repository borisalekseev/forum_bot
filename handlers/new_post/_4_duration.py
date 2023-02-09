import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Regexp

from states import NewPost
from config import dp
import messages


@dp.message_handler(Regexp(r'\d{1,3}'), state=NewPost.duration)
async def duration_choice(message: types.Message, state: FSMContext):
    duration = int(message.text)
    await state.update_data(duration=duration)
    post_data = await state.get_data()

    # plan task, save it

    await state.finish()
    await message.answer(messages.NEW_POST_SUCCESS)


@dp.message_handler(state=NewPost.duration)
async def date_choice_bad(message: types.Message):
    await message.answer(messages.NEW_POST_BAD)
