import datetime
from db.db_api import db_api


# Проверяем выходит ли сегодня какая-либо новая серия аниме
def send_today(current_date: str) -> bool:
    release_dates = db_api().get_anime_releases()
    for date in release_dates:
        if current_date in date:
            return True


# Получаем тайтлы, которые выходят сегодня
def get_titles(current_date: str) -> tuple:
    titles = db_api().get_anime_titles(current_date)
    return titles


async def run() -> tuple:
    dt = datetime.datetime.now().strftime("%#d-%m-%Y")
    result = get_titles(dt) if send_today(dt) else None
    return result







