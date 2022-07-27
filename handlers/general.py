from aiogram import types
from loader import dp
from db.db_api import db_api


# Проверяем имеется ли сериал в списке отслеживаемого у пользователя
def check_title(title, target_titles):
    for element in target_titles:
        if title in element:
            return True
    return False

# Команда /info - Выводим список всех сериалов, который добавил к себе пользователь
@dp.message_handler(commands=['info'])
async def process_info_command(message: types.Message):
    user_info = db_api().get_user_info(message.from_user.id)
    titles = db_api().get_user_serial_info(user_info.id)
    for title in titles:
        await message.answer(f"Название: {title[0]}\n"
                             f"Рейтинг IMDB: {title[1]} из 10\n"
                             f"Жанры: {title[2]}.")


# Команда /delete - Удаляем сериал из списка отслеживаемого
@dp.message_handler(commands=['delete'])
async def process_info_command(message: types.Message):
    user_info = db_api().get_user_info(message.from_user.id)
    target_titles = db_api().get_user_serial_info(user_info.id)

    title = str(message.text[8:]).strip()

    if title != "":
        if check_title(title, target_titles):
            db_api().delete_serial(user_info.id, title)
            await message.answer(f"Сериал {title} удален из списка отслеживаемого.")
        else:
            await message.answer(f"Сериал {title} не находится в вашем списке отслеживаемого.")
    else:
        await message.answer(f"Неправильно используется команда /delete, воспользуйтесь /help для того,"
                             f" чтобы ознакомиться с возможностями бота.")
