import datetime

import aioschedule
import asyncio
from database import Post, PostTask
from utils import PostInfo


async def plane_posts(data: PostInfo) -> None:
    """Takes post data from FSMContext and create the nearest task & writes it to base"""
    post = await Post.create(
        text=data.text,
        photos=data.photos
    )


async def useless():
    print('asdasd')


if __name__ == "__main__":
    aioschedule.every(5).seconds.do(plane_posts, PostInfo('123', ['qwe'], [datetime.time(hour=1)], 2))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(aioschedule.run_pending())
