from datetime import date
import datetime
import selenium.common
from parser.init_parser import Parser
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# Класс для парсинга метаданных определенного аниме
class Anime(Parser):

    # Парсим результаты поиска
    def parse_page(self, title):
        self.driver.get(self.url)

        input = self.driver.find_element(By.CLASS_NAME, "form-control-lg").find_element(By.TAG_NAME, "input")
        input.send_keys(title)
        input.send_keys(Keys.ENTER)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "search-county"))
        )

        switch_to = self.driver.find_elements(By.CLASS_NAME, "nav-link")

        for element in switch_to:
            try:
                if element.find_element(By.CLASS_NAME, "text-link-gray").text:
                    element.click()
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "active"))
                    )
                    break
            except selenium.common.exceptions.NoSuchElementException:
                pass

        titles = self.driver.find_elements(By.CLASS_NAME, "animes-grid-item")

        return titles

    # Проверяем есть ли такое аниме
    @staticmethod
    def is_valid_title(title, titles):
        for element in titles:
            if title.lower() in element.find_element(By.CLASS_NAME, "card-title").text.lower():
                return title

    # Проверяем статус аниме
    def is_valid_status(self, title):
        titles = self.driver.find_elements(By.CLASS_NAME, "card-title")

        for element in titles:
            if element.text == title:
                element.find_element(By.LINK_TEXT, title).click()
                break

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "anime-info"))
        )

        anime_info = self.driver.find_element(By.CLASS_NAME, "anime-info").find_elements(By.CLASS_NAME, "col-sm-8")

        for attr in anime_info:
            if attr.text == "Онгоинг":
                return True

    # Собираем данные о аниме
    def parse_title(self):
        pass

    def run(self, title):
        titles = self.parse_page(title)
        if self.is_valid_title(title, titles):
            print(self.is_valid_status(title))
        else:
            print("Неправильное название!!!")



