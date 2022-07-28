from aiogram import types
from loader import dp
from parser.anime import Anime
from db.db_api import db_api


# Команда /add_anime - добавляет аниме в БД
@dp.message_handler(commands=['add_anime'])
async def process_add_anime_command(message: types.Message):

    title = str(message.text[11:]).strip()

    anime = Anime("https://animego.org/search/all?q=")
    anime.run(title)

    await message.answer("Я буду добавлять аниме в БД!")