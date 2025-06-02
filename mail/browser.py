import time

import allure
from selenium import webdriver


class Browser:


    def __init__(self, url):
        self.url = url
        self.options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=self.options)
        self.open_url_from_message()


    @allure.step('Открытие URL из сообщения')
    def open_url_from_message(self):

        """Открываем URL из сообщения в браузере"""

        allure.attach(self.url, 'URL для открытия')  # Логируем URL перед открытием
        self.driver.get(self.url)
        time.sleep(2)
        allure.attach('Страница загружена', 'Статус загрузки страницы')  # Логируем статус загрузки
        self.driver.quit()


