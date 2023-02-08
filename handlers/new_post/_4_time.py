from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Regexp

from config import dp, STRPTIME_PATTERN
from states import NewPost
import messages


@dp.message_handler(Regexp(r'\d\d:\d\d'), state=NewPost.time)
async def time_choice(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        post_datetime_string = data["date_string"] + ' ' + message.text
        post_datetime = datetime.strptime(post_datetime_string, STRPTIME_PATTERN)
        data.update(post_datetime=post_datetime, post_datetime_string=post_datetime_string)
    await state.finish()

    await message.answer(messages.NEW_POST_SUCCESS)


@dp.message_handler(content_types=types.ContentType.ANY, state=NewPost.time)
async def time_choice_bad(message: types.Message):
    await message.answer(messages.NEW_POST_BAD + '\n' + messages.NEW_POST_TIME)
