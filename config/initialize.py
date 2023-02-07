from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from .const import TOKEN


bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
