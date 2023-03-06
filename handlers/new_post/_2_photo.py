from aiogram import types
from aiogram.dispatcher import FSMContext

import messages
from states import NewPost
from config import dp


@dp.message_handler(content_types=types.ContentType.PHOTO, state=NewPost.photo)
async def new_post_photo(message: types.Message, state: FSMContext, album: list[str] = None):
    """
    :param state:
    :param message:
    :param album:  middlewares.album.AlbumMiddleware передаёт список file_id (в самом лучшем доступном качестве)
    Если будет отправлено одно фото, обработает так же, как и middleware
    """
    if album is None:
        album = [message.photo[-1].file_id]
    await state.update_data(photo=album)
    await NewPost.next()

    await message.answer(messages.NEW_POST_TIME)


@dp.message_handler(state=NewPost.photo)
async def photo_bad(message: types.Message, state: FSMContext, album: list[str] = None):
    await message.answer(messages.NEW_POST_BAD)
