from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext

from config import dp
from states import NewPost
import messages


@dp.message_handler(Command("new_post"))
async def new_post(message: types.Message, state: FSMContext):
    await message.answer(messages.NEW_POST_TEXT)
    await state.set_state(NewPost.text)


@dp.message_handler(state=NewPost.text)
async def new_post_text(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer(messages.NEW_POST_MEDIA)
    await state.set_state(await NewPost.next())


@dp.message_handler(content_types=["photo"], state=NewPost.media)
async def new_post_text(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    await message.answer_photo(message.photo[-1].file_id)
