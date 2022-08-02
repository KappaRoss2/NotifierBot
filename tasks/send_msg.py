from db.db_api import db_api
from tasks.anime_check import run
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loader import bot
from parser.anime import Anime
import datetime


# Изменяем данные в таблице anime_titles
def update_anime_table(target_titles: tuple):
    for title in target_titles:
        anime = Anime("https://animego.org/search/all?q=")
        result = anime.run(title)
        if type(result) is list and result is not None:
            db_api().update_anime_table(result[3], result[0])
        elif type(result) is str:
            db_api().delete_column_anime(result[0])


# Отправляем сообщение пользователям
async def send_msg():
    target_titles = await run()
    today = datetime.datetime.now().strftime("%#d-%m-%Y")
    if target_titles:
        users = db_api().get_userid_anime_notify(today)
        for user in users:
            user_titles = db_api().get_user_anime_info(user)
            for title in user_titles:
                if title[0] in target_titles:
                    chat_id = db_api().get_userid_for_bot(user)[0]
                    await bot.send_message(chat_id, f"Сегодня выйдет новая серия аниме \"{title[0]}\"!")
        update_anime_table(target_titles)


# Запускаем функцию send_msg с интервалом в один день.
scheduler = AsyncIOScheduler()
scheduler.add_job(send_msg, "interval", days=1)

scheduler.start()
