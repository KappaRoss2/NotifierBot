import sqlite3


class db_api:

    def __init__(self):
        self.conn = sqlite3.connect("db\\notifier.db")
        self.cur = self.conn.cursor()

    def add_user(self, data: tuple):
        self.cur.execute("INSERT INTO users(user_id, user_name) VALUES (?, ?);", data)
        self.conn.commit()

    def check_users(self, user_id):
        self.cur.execute("SELECT * from users WHERE user_id=?;", (user_id, ))
        return self.cur.fetchone()



