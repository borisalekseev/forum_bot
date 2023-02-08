from aiogram.dispatcher.filters.state import State, StatesGroup


class NewPost(StatesGroup):
    text = State()
    photo = State()
    date = State()
    time = State()
