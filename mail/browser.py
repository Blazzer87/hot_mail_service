import time

from selenium import webdriver


class Browser:

    def __init__(self, url):
        self.url = url
        self.options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=self.options)
        self.open_url_from_message()

    def open_url_from_message(self):
        # self.options.page_load_strategy = 'eager'     # не всегда нужна, написана больше для дебага
        self.driver.get(self.url)
        self.driver.quit()


