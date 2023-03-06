from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Regexp

from config import dp
from utils import TimeValidationError, validate_time
from states import NewPost
import messages


@dp.message_handler(Regexp(r'\d\d:\d\d( \d\d:\d\d)*\s?'), state=NewPost.times)
async def time_choice(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        times = validate_time(message.text.strip().split())
        post_times = times
        data.update(times=post_times)

    await NewPost.next()
    await message.answer(messages.NEW_POST_DURATION_DAYS)


@dp.errors_handler(exception=TimeValidationError)
@dp.message_handler(content_types=types.ContentType.ANY, state=NewPost.times)
async def time_choice_bad(message: types.Message):
    await message.answer(messages.NEW_POST_BAD + '\n' + messages.NEW_POST_TIME)
