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

    # Добавляем сериал в таблицу serial_titles
    def add_serial(self, data: list):
        self.cur.execute("INSERT INTO serial_titles(user_id, title, rating_imdb, genres, releases) "
                         "VALUES (?, ?, ?, ?, ?);", data)
        self.conn.commit()

    # Получаем сериалы, которые добавил пользователь к себе в список
    def get_user_title(self, user_id: str) -> tuple:
        self.cur.execute("SELECT title FROM serial_titles WHERE user_id=?;", (user_id, ))

        result = ()
        for title in self.cur.fetchall():
            result += title

        return result

    # Получаем данные о сериалах, которые отслеживает определенный пользователь
    def get_user_serial_info(self, user_id: str) -> list:
        self.cur.execute("SELECT title, rating_imdb, genres FROM serial_titles WHERE user_id=?;", (user_id,))
        return self.cur.fetchall()

    # Удаляем сериал из отслеживаемого у определенного пользователя
    def delete_serial(self, user_id: str, title: str):
        self.cur.execute("DELETE FROM serial_titles WHERE user_id=? and title=?;", (user_id, title, ))
        self.conn.commit()

    # Получаем даты всех релизов сериалов
    def get_serial_releases(self) -> list:
        self.cur.execute("SELECT DISTINCT releases FROM serial_titles")
        return self.cur.fetchall()

    # Получаем тайтлы, которые выходят в определенную дату
    def get_serial_titles(self, date: str) -> tuple:
        self.cur.execute("SELECT DISTINCT title FROM serial_titles WHERE releases = ?;", (date,))

        data = ()

        for fetch in self.cur.fetchall():
            data += fetch

        return data

    # Получаем user_id пользователей, которым нужно будет отправлять уведомление
    def get_userid_serial_notify(self, date: str) -> tuple:
        self.cur.execute("SELECT DISTINCT user_id FROM serial_titles WHERE title "\
                         "IN (SELECT DISTINCT title FROM serial_titles WHERE releases = ?);", (date,))
        data = ()
        for fetch in self.cur.fetchall():
            data += fetch

        return data

    # Обновляем данные о сериале
    def update_serial_table(self, date: str, title: str):
        self.cur.execute("UPDATE serial_titles SET releases=? WHERE title=?", (date, title,))
        self.conn.commit()

    # Удаляем данные по определенному сериалу
    def delete_column_serial(self, title: str):
        self.cur.execute("DELETE FROM serial_titles WHERE title=?", (title,))
        self.conn.commit()

    # Добавляем аниме в таблицу anime_titles
    def add_anime(self, data: list):
        self.cur.execute("INSERT INTO anime_titles(user_id, title, genres, rating, release) "
                         "VALUES (?, ?, ?, ?, ?);", data)
        self.conn.commit()

    # Получаем данные о аниме, которые отслеживает пользователь
    def get_user_anime_info(self, user_id: str) -> list:
        self.cur.execute("SELECT title, genres, rating, release "
                         "FROM anime_titles WHERE user_id=?;", (user_id,))
        return self.cur.fetchall()

    # Удаляем аниме из отслеживаемого у определенного пользователя
    def delete_anime(self, user_id: str, title: str):
        self.cur.execute("DELETE FROM anime_titles WHERE user_id=? and title=?;", (user_id, title, ))
        self.conn.commit()

    # Получаем даты всех релизов аниме
    def get_anime_releases(self) -> list:
        self.cur.execute("SELECT DISTINCT release FROM anime_titles WHERE title IN (SELECT title FROM anime_titles);")
        return self.cur.fetchall()

    # Получаем все тайтлы, которые выходят в определенную дату
    def get_anime_titles(self, date: str) -> tuple:
        self.cur.execute("SELECT DISTINCT title FROM anime_titles WHERE release = ?;", (date, ))

        data = ()

        for fetch in self.cur.fetchall():
            data += fetch

        return data

    # Получаем user_id пользователей, которым нужно будет отправлять уведомление
    def get_userid_anime_notify(self, date: str) -> tuple:
        self.cur.execute("SELECT DISTINCT user_id FROM anime_titles WHERE title "\
                         "IN (SELECT DISTINCT title FROM anime_titles WHERE release = ?);", (date, ))
        data = ()
        for fetch in self.cur.fetchall():
            data += fetch

        return data

    # Получаем id чата с телеграмм ботом
    def get_userid_for_bot(self, user: int):
        self.cur.execute("SELECT user_id FROM users WHERE id = ?", (user, ))
        return self.cur.fetchone()

    # Изменяем значение в таблице anime_titles
    def update_anime_table(self, date: str, title: str):
        self.cur.execute("UPDATE anime_titles SET release=? WHERE title=?", (date, title, ))
        self.conn.commit()

    # Удаляем данные по определенному аниме
    def delete_column_anime(self, title: str):
        self.cur.execute("DELETE FROM anime_titles WHERE title=?", (title, ))
        self.conn.commit()

