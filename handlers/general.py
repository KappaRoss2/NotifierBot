from aiogram import types
from loader import dp
from db.db_api import db_api


# Команда /info - Выводим список всех сериалов, который добавил к себе пользователь
@dp.message_handler(commands=['info'])
async def process_info_command(message: types.Message):
    user_info = db_api().get_user_info(message.from_user.id)
    titles = db_api().get_user_serial_info(user_info.id)
    for title in titles:
        await message.answer(f"Название: {title[0]}\n"
                             f"Рейтинг IMDB: {title[1]} из 10\n"
                             f"Жанры: {title[2]}.")
