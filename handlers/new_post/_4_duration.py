from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Regexp

from states import NewPost
from config import dp
import messages
from utils import topics_select


@dp.message_handler(Regexp(r'\d{1,3}'), state=NewPost.duration)
async def duration_choice(message: types.Message, state: FSMContext):
    duration = int(message.text)
    await state.update_data(duration=duration)

    await NewPost.next()
    await message.answer(messages.NEW_POST_TOPICS, reply_markup=topics_select())


@dp.message_handler(state=NewPost.duration)
async def date_choice_bad(message: types.Message):
    await message.answer(messages.NEW_POST_BAD)
