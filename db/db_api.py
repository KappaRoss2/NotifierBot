import sqlite3

# Класс для работы с БД


class db_api:

    # Подключаемся к нашей БД
    def __init__(self):
        self.conn = sqlite3.connect("db\\notifier.db")
        self.cur = self.conn.cursor()

    # Добавляем пользователя в БД
    def add_user(self, data: tuple):
        self.cur.execute("INSERT INTO users(user_id, user_name) VALUES (?, ?);", data)
        self.conn.commit()

    # Получаем информацию об определенном пользователя с id = user_id
    def get_user_info(self, user_id):
        self.cur.execute("SELECT * from users WHERE user_id=?;", (user_id, ))
        return self.cur.fetchone()

    # Добавляем сериал в таблицу serial_titles
    def add_serial(self, data):
        self.cur.execute("INSERT INTO serial_titles(user_id, title, rating_imdb, genres, releases) "
                         "VALUES (?, ?, ?, ?, ?);", data)
        self.conn.commit()




