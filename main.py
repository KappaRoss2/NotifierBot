import config
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from handlers.intro import process_start_command
from handlers.serials import process_add_serial_command
from loader import dp


if __name__ == '__main__':
    executor.start_polling(dp)