import asyncio
import datetime

from aiogram import types

from database import Post, PostTask
from utils import PostInfo
from config import bot


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
        photos=data.photos
    )
    now = datetime.datetime.now()
    for time in data.times:
        if time > now.time():
            task_date = now.date() + datetime.timedelta(days=1)
            first_datetime = datetime.datetime.combine(task_date, time)
        else:
            first_datetime = datetime.datetime.combine(
                now.date() + datetime.timedelta(hours=time.hour, minutes=time.minute), time
            )

        await create_post_tasks(post.id, first_datetime, data.duration)


async def create_post_tasks(post_id: int, first_datetime: datetime.datetime, duration: int, topics: str) -> None:
    for day in range(duration):
        await PostTask.create(
            post_id=post_id,
            datetime=first_datetime + datetime.timedelta(days=day),
            topics=topics
        )


async def on_start_tasks():

    async for post_task in PostTask.filter(done=False, planned=False, failed=False):
        now = datetime.datetime.now()
        if post_task.datetime < now:
            post_task.planned = True
            await post_task.save()
            await do_post(post_task.post_id, post_task.id, post_task.topics.split('|'), at=post_task.datetime)
        else:
            post_task.failed = True
            await post_task.save()


async def on_shutdown_tasks(dp):
    async for post_task in PostTask.filter(done=False, planned=True, failed=False):
        post_task.planned = False
        await post_task.save()


async def do_post(post_id: int, task_id: int, topics: list[str], at: datetime.datetime = None):
    post = await Post.get(id=post_id)
    media = [types.InputMediaPhoto(media=file_id) for file_id in post.photos]
    seconds_to_sleep = at - datetime.datetime.now()
    await asyncio.sleep(seconds_to_sleep.total_seconds())
    for topic in topics:
        await bot.send_media_group(chat_id=int(topic), caption=post.text, media=media)

    task = await PostTask.get(id=task_id)
    task.done = True
    await task.save()


async def check_new_posts():
    await asyncio.sleep(10)
    while True:
        async for post_task in PostTask.filter(done=False, planned=False, failed=False):
            await do_post(post_task.post_id, post_task.id, post_task.topics.split('|'), at=post_task.datetime)
        await asyncio.sleep(10)
