import asyncio
import datetime
import pytz

from aiogram import types
from aiogram.types import MediaGroup

from database import Post, PostTask
from utils import PostInfo
from config import bot, FORUM_CHAT_ID

tz = pytz.timezone('UTC')


async def wait_for_datetime(wait_for: datetime.datetime):
    interval = wait_for - datetime.datetime.now()
    if interval.seconds < 0:
        # ToDo warning / processing
        return
    await asyncio.sleep(interval.seconds)


async def plane_posts(data: PostInfo):
    """Takes post data from FSMContext and create the nearest task & writes it to base"""
    post = await Post.create(
        text=data.text,
        photos=data.photo
    )
    now = datetime.datetime.now()
    for time in data.times:
        if time < now.time():
            task_date = now.date() + datetime.timedelta(days=1)
            first_datetime = datetime.datetime.combine(task_date, time)
        else:
            first_datetime = datetime.datetime.combine(
                now.date() + datetime.timedelta(hours=time.hour, minutes=time.minute), time
            )

        await create_post_tasks(post.id, first_datetime, data.duration, data.topics)


async def create_post_tasks(post_id: int, first_datetime: datetime.datetime, duration: int, topics: str) -> None:
    for day in range(duration):
        await PostTask.create(
            post_id_id=post_id,
            datetime=first_datetime + datetime.timedelta(days=day),
            topics=topics
        )


async def on_start_tasks():

    async for post_task in PostTask.filter(done=False, planned=False, failed=False):
        now = datetime.datetime.now().timestamp()
        if post_task.datetime.timestamp() < now:
            post_task.planned = True
            await post_task.save()
            await do_post(post_task.post_id_id, post_task.id, post_task.topics.split('|'), at=post_task.datetime)
        else:
            post_task.failed = True
            await post_task.save()


async def on_shutdown_tasks(dp):
    async for post_task in PostTask.filter(done=False, planned=True, failed=False):
        post_task.planned = False
        await post_task.save()


async def do_post(post_id: int, task_id: int, topics: list[str], at: datetime.datetime = None):
    post = await Post.get(id=post_id)
    media = MediaGroup()
    for file_id in post.photos:
        media.attach_photo(types.InputMediaPhoto(media=file_id), caption=post.text)
    now = tz.localize(datetime.datetime.now())
    seconds_to_sleep = at - now
    await asyncio.sleep(seconds_to_sleep.total_seconds())
    for topic in topics:
        thread_id = None if topic == "None" else int(topic)
        await bot.send_media_group(chat_id=FORUM_CHAT_ID, media=media, message_thread_id=thread_id)
        await bot.send_message(chat_id=FORUM_CHAT_ID, text=post.text, message_thread_id=thread_id)

    task = await PostTask.get(id=task_id)
    task.done = True
    await task.save()


async def check_new_posts():
    await asyncio.sleep(2)
    while True:
        async for post_task in PostTask.filter(done=False, planned=False, failed=False):
            await do_post(post_task.post_id_id, post_task.id, post_task.topics.split('|'), at=post_task.datetime)
        await asyncio.sleep(10)
