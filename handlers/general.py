from aiogram import types
from loader import dp
from parser.serials import Serials
from db.db_api import db_api


# Команда /info - Выводим список всех сериалов, который добавил к себе пользователь
@dp.message_handler(commands=['info'])
async def process_help_command(message: types.Message):
    pass