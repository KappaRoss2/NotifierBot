from datetime import date
import selenium.common.exceptions
from parser.init_parser import parser
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class Serials(parser):

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

    def is_valid_title(self, title):
        check_title = self.driver.find_elements(By.CLASS_NAME, "Row")
        for element in check_title:
            if title in element.text:
                return element

    @staticmethod
    def is_valid_status(element):
        try:
            status = element.find_element(By.CLASS_NAME, "_dead")
        except selenium.common.exceptions.NoSuchElementException:
            status = "Fine"

        return status

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

        data = [name, rating, genres]

        return data

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
