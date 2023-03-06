from aiogram.dispatcher.filters.state import State, StatesGroup


class NewPost(StatesGroup):
    text = State()
    photo = State()
    times = State()
    duration = State()
    topics = State()
