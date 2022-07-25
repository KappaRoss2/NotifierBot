from selenium import webdriver
from selenium_stealth import stealth
from db.db_api import db_api


# Инициализируем родительский класс Parser
class Parser:

    # Констуктор в котором формируется сессия
    def __init__(self, url: str):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(options=options, executable_path='parser/chromedriver.exe')

        stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )
        self.url = url
        self.result = []

    # Сохраняем сериал в БД
    @staticmethod
    def save(user_id, data: list):
        user_info = db_api()
        user_id = user_info.get_user_info(user_id)[0]
        data.insert(0, user_id)
        user_info.add_serial(data)




