from tortoise import Tortoise
from config import TORTOISE_CONFIG


async def init():
    await Tortoise.init(
        config=TORTOISE_CONFIG
    )
    await Tortoise.generate_schemas()
