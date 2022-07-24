from aiogram import types
from loader import dp
from db.db_api import db_api
from datetime import datetime
from parser.serials import Serials


@dp.message_handler(commands=['add_serial'])
async def process_add_serial_command(message: types.Message):

    serial = Serials("https://myshows.me/search/all/")
    result = serial.run(message.text[12:])

    if type(result) is str:
        await message.answer(result)

    print(result)

    await message.answer("Я буду добавлять сериал в Базу данных!!!")