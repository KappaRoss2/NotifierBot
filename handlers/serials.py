from aiogram import types
from loader import dp
from parser.serials import Serials
from db.db_api import db_api


# Команда /add_serial - добавляет сериал в БД
@dp.message_handler(commands=['add_serial'])
async def process_add_serial_command(message: types.Message):

    title = str(message.text[12:]).strip()

    if title != "":
        await message.answer(f"Тааак, сейчас посмотрим...")
        user_info = db_api().get_user_info(message.from_user.id)
        title_info = db_api().get_user_title(user_info.id)

        if title not in title_info:
            serial = Serials("https://myshows.me/search/all/")
            result = serial.run(title)

            if type(result) is str:
                await message.answer(result)
            else:
                result.insert(0, user_info.id)
                db_api().add_serial(result)
                await message.answer(f"Сериал {result[1]} добавлен в ваш список!")
        else:
            await message.answer(f"Сериал {title} уже есть в вашем списке")
    else:
        await message.answer(f"Неправильно используется команда /add_serial, воспользуйтесь командой /help "
                             f"чтобы ознакомиться с возможностями бота.")