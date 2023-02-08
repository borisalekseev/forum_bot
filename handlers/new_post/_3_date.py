import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from aiogram_datepicker import Datepicker, DatepickerSettings

from states import NewPost
from config import dp
import messages


def _get_datepicker_settings():
    return DatepickerSettings()


@dp.callback_query_handler(Datepicker.datepicker_callback.filter(), state=NewPost.date)
async def date_choice(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    datepicker = Datepicker(_get_datepicker_settings())
    date: bool | datetime.date = await datepicker.process(call, callback_data)
    # не понятно, что там с типизацией, но второй аргумент должен быть dict, в библиотеку лезть не стал.

    if date is False:
        return

    await state.update_data(date_string=str(date))
    await NewPost.next()
    await call.message.answer(messages.NEW_POST_TIME)


@dp.callback_query_handler(Datepicker.datepicker_callback.filter())
async def date_choice_bad_call(call: types.CallbackQuery):
    await call.answer(messages.CALENDAR_BAD_CALL)


@dp.message_handler(state=NewPost.date)
async def date_choice_bad(message: types.Message):
    await message.answer(messages.NEW_POST_BAD)
