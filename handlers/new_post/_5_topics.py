from aiogram import types
from aiogram.dispatcher import FSMContext

from states import NewPost
from config import dp
import messages
from utils import PostInfo, get_topics, change_topics

from jobs import plane_posts


@dp.callback_query_handler(state=NewPost.topics)
async def topics_choice(call: types.CallbackQuery, state: FSMContext):
    if call.data == "choose_topic_ready":
        topics = '|'.join(get_topics(call.message.reply_markup.inline_keyboard))
        await state.update_data(topics=topics)
        post_dict = await state.get_data()
        post_data = PostInfo(**post_dict)
        await plane_posts(post_data)

        await state.finish()
        return await call.message.answer(messages.NEW_POST_SUCCESS)

    print(call.data)

    _, key, str_condition = call.data.split("|")
    condition = True if str_condition == "true" else False
    keyboard = call.message.reply_markup
    new_keyboard = change_topics(keyboard, key, condition)
    await call.message.edit_reply_markup(reply_markup=new_keyboard)


@dp.message_handler(state=NewPost.topics)
async def topics_choice_bad(message: types.Message):
    await message.answer(messages.NEW_POST_BAD)
