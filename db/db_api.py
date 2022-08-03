import sqlite3
import collections


# Класс для работы с БД
class db_api:

    # Подключаемся к нашей БД
    def __init__(self):
        self.conn = sqlite3.connect("db/notifier.db")
        self.cur = self.conn.cursor()

    # Добавляем пользователя в БД
    def add_user(self, data: tuple):
        self.cur.execute("INSERT INTO users(user_id, user_name) VALUES (?, ?);", data)
        self.conn.commit()

    # Получаем информацию об определенном пользователя с id = user_id
    def get_user_info(self, user_id: str) -> list or None:
        self.cur.execute("SELECT * from users WHERE user_id=?;", (user_id, ))
        result = self.cur.fetchone()

        if result is not None:
            data = collections.namedtuple('User', ['id', 'user_id', 'join_date', 'user_name'])
            data = data(id=result[0], user_id=result[1], join_date=result[2], user_name=result[3])
            return data
        else:
            return result

    # Получаем id чата с телеграмм ботом
    def get_userid_for_bot(self, user: int):
        self.cur.execute("SELECT user_id FROM users WHERE id = ?", (user, ))
        return self.cur.fetchone()

