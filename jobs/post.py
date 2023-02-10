import asyncio
import datetime

from database import Post, PostTask
from utils import PostInfo
from config import bot


async def wait_for_datetime(wait_for: datetime.datetime) -> None:
    interval = wait_for - datetime.datetime.now()
    if interval.seconds < 0:
        # ToDo warning / processing
        return
    await asyncio.sleep(interval.seconds)


async def plane_posts(data: PostInfo) ->  None:
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

        await create_post_tasks(post.id, first_datetime, PostInfo.duration)


async def create_post_tasks(post_id: int, first_datetime: datetime.datetime, duration: int) -> None:
    for day in range(duration):
        await PostTask.create(
            post_id=post_id,
            datetime=first_datetime + datetime.timedelta(days=day)
        )


async def create_start_tasks():
    now = datetime.datetime.now()
    planned = set()

    async for post_task in PostTask.filter(done=False):
        if post_task.datetime < now:
            await do_post(post_task.post_id, post_task.topics.split('|'))
            planned.add(post_task.post_id)

    async for post_task in PostTask.filter(done=False).exclude(id__in=list(planned)):
        if post_task.post_id in planned:
            continue
        await do_post(post_task.post_id, post_task.topics.split('|'), at=post_task.datetime)


async def do_post(post_id: int, topics: list[str], at: datetime = None) -> None:
    bot.send_