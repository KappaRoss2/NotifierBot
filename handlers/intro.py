from aiogram import types
from loader import dp
from db.db_api import db_api
from datetime import datetime


# Команда /start - добавляем пользователя в БД
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    data = (message.from_user.id, message.from_user.username)
    user_info = db_api()
    check = user_info.get_user_info(data[0])

    if check is not None:
        date = datetime.strptime(check[2], "%Y-%m-%d %H:%M:%S")
        await message.answer("Мне кажется или ты уже регистрировался " + date.strftime("%d %b %Y") + " в "
                             + date.strftime("%H:%M:%S") +" ?")
    else:
        user_info.add_user(data)
        await message.answer("Привет, теперь я буду уведомлять тебя о выходе новых серий, воспользуйся командой"
                             " /help чтобы посмотреть, что я умею")


# Команда /help - Выводим список всех возможных команд
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.answer("/add_serial [Название сериала] - добавляет сериал в список отслеживаемого")