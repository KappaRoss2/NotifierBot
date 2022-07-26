from datetime import date
import datetime
import selenium.common.exceptions
from parser.init_parser import Parser
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# Класс для парсинга метаданных определенного сериала
class Serials(Parser):

    # Парсим результаты поиска
    def parse_page(self, title):

        self.driver.get(self.url)

        input = self.driver.find_element(By.CLASS_NAME, "SearchField-input")
        input.send_keys(title)
        input.send_keys(Keys.ENTER)

        handler = self.driver.current_window_handle
        self.driver.switch_to.window(handler)

        time.sleep(1)

        element = self.is_valid_title(title)

        if element is not None:
            return element

    # Проверяем существует ли такой сериал в принципе
    def is_valid_title(self, title):
        check_title = self.driver.find_elements(By.CLASS_NAME, "Row")
        for element in check_title:
            if title in element.text:
                return element

    # Проверяем выпускается ли сериал, зачем следить за сериалом, который итак закрыт?
    @staticmethod
    def is_valid_status(element):
        try:
            status = element.find_element(By.CLASS_NAME, "_dead")
        except selenium.common.exceptions.NoSuchElementException:
            status = "Fine"

        return status

    # Собираем данные о сериале
    def parse_title(self):
        name = self.driver.find_element(By.CLASS_NAME, "title__main").text
        attrs = self.driver.find_elements(By.CLASS_NAME, "info-row")

        genres = None
        rating = None

        for attr in attrs:
            if "Жанры" in attr.text:
                genres = attr.text[7:]

            if "Рейтинг IMDB" in attr.text:
                rating = attr.text[14:attr.text.find("из") - 1]

        release = self.get_release()

        data = [name, rating, genres, release]

        return data

    # Отдельный метод для получения списка дат выхода следующих серий
    def get_release(self):
        self.driver.find_element(By.CLASS_NAME, "episodes-by-season__season-row_toggle-icon").click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "episode-col__date"))
        )

        release = self.driver.find_elements(By.CLASS_NAME, "episode-col__date")

        release_dates = [element.text for element in release if element.text != "" and element.text != "вчера"
                         and element.text != "сегодня"]

        release_dates = ", ".join([str(datetime.datetime.strptime(element, '%d.%m.%Y').date()) for element in release_dates
                         if datetime.datetime.strptime(element, '%d.%m.%Y').date() > date.today()])

        print(release_dates)

        return release_dates

    # Складываем все воедино
    def run(self, title):
        element = self.parse_page(title)
        if element:
            if self.is_valid_status(element) == "Fine":
                element.find_element(By.TAG_NAME, "a").click()

                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "ShowDetails-poster"))
                )

                window = self.driver.current_window_handle
                self.driver.switch_to.window(window)

                data = self.parse_title()

                return data

            else:
                return "Сериал уже давно закрыли, чеееееееел"
        else:
            return "Не знаю такого сериала"