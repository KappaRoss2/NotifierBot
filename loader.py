from aiogram import Bot, Dispatcher
import config


bot = Bot(token=config.token)
dp = Dispatcher(bot)
