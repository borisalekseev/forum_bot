from aiogram import types
from aiogram.dispatcher import FSMContext

import messages
from states import NewPost
from config import dp


@dp.message_handler(state=NewPost.text)
async def text(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer(messages.NEW_POST_PHOTO)
    await NewPost.next()


@dp.message_handler(state=NewPost.text)
async def text_wrong(message: types.Message, state: FSMContext):
    await message.answer(messages.NEW_POST_BAD)
