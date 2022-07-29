import datetime
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
    def get_user_info(self, user_id):
        self.cur.execute("SELECT * from users WHERE user_id=?;", (user_id, ))
        result = self.cur.fetchone()

        if result is not None:
            data = collections.namedtuple('User', ['id', 'user_id', 'join_date', 'user_name'])
            data = data(id=result[0], user_id=result[1], join_date=result[2], user_name=result[3])
            return data
        else:
            return result

    # Добавляем сериал в таблицу serial_titles
    def add_serial(self, data):
        self.cur.execute("INSERT INTO serial_titles(user_id, title, rating_imdb, genres, releases) "
                         "VALUES (?, ?, ?, ?, ?);", data)
        self.conn.commit()

    # Получаем сериалы, которые добавил пользователь к себе в список
    def get_user_title(self, user_id):
        self.cur.execute("SELECT title FROM serial_titles WHERE user_id=?;", (user_id, ))

        result = ()
        for title in self.cur.fetchall():
            result += title

        return result

    # Получаем данные о сериалах, которые отслеживает определенный пользователь
    def get_user_serial_info(self, user_id):
        self.cur.execute("SELECT title, rating_imdb, genres FROM serial_titles WHERE user_id=?;", (user_id,))
        return self.cur.fetchall()

    # Удаляем сериал из отслеживаемого у определенного пользователя
    def delete_serial(self, user_id, title):
        self.cur.execute("DELETE FROM serial_titles WHERE user_id=? and title=?;", (user_id, title, ))
        self.conn.commit()

    # Добавляем аниме в таблицу anime_titles
    def add_anime(self, data):
        self.cur.execute("INSERT INTO anime_titles(user_id, title, genres, rating, release) "
                         "VALUES (?, ?, ?, ?, ?);", data)
        self.conn.commit()

    # Получаем данные о аниме, которые отслеживает пользователь
    def get_user_anime_info(self, user_id):
        self.cur.execute("SELECT title, genres, rating, release "
                         "FROM anime_titles WHERE user_id=?;", (user_id,))
        return self.cur.fetchall()

    # Удаляем аниме из отслеживаемого у определенного пользователя
    def delete_anime(self, user_id, title):
        self.cur.execute("DELETE FROM anime_titles WHERE user_id=? and title=?;", (user_id, title, ))
        self.conn.commit()







