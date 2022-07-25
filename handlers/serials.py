from aiogram import types
from loader import dp
from parser.serials import Serials


# Команда /add_serial - добавляет сериал в БД
@dp.message_handler(commands=['add_serial'])
async def process_add_serial_command(message: types.Message):

    await message.answer(f"Тааак, сейчас посмотрим, подожди немного пожалуйста.")
    serial = Serials("https://myshows.me/search/all/")
    result = serial.run(message.text[12:])

    if type(result) is str:
        await message.answer(result)

    serial.save(message.from_user.id, result)

    await message.answer(f"Сериал {result[1]} добавлен в ваш список!")