import email
import re
from email.header import decode_header
from email.utils import parseaddr, parsedate_to_datetime
import allure
from mail.browser import Browser


class MailMessage:

    msg: email.message.Message


    def __init__(self, msg: email.message.Message):
        self.msg = msg
        self.body = None



    @allure.step('Получение имени отправителя')
    def get_sender_name(self):

        """Декодируем заголовок "От" и получаем имя отправителя"""

        with allure.step('Чтение заголовка "От"'):
            sender_header = self.msg['From']
            allure.attach(sender_header, 'Заголовок "От"')  # Логируем заголовок "От"

            sender_name = decode_header(sender_header)[0][0]
            allure.attach(str(sender_name), 'Исходное имя отправителя')  # Логируем исходное имя

            if isinstance(sender_name, bytes):
                sender_name = sender_name.decode()

            sender_name = self.extract_sender_name(sender_name)

            allure.attach(sender_name, 'Извлеченное имя отправителя')  # Логируем извлеченное имя
            return sender_name



    @allure.step('Извлечение имени отправителя')
    def extract_sender_name(self, sender_name: str) -> str:

        """Вспомогательная функция "извлекатель" - получает имя отправителя, очищая от лишнего"""

        allure.attach(sender_name, 'Исходное имя отправителя')  # Логируем исходное имя отправителя

        match = re.search(r'<([^>]+)>', sender_name)
        if match:
            extracted_name = match.group(1)
            allure.attach(extracted_name, 'Извлеченное имя отправителя')  # Логируем извлеченное имя
            return extracted_name

        cleaned_name = sender_name.strip()
        allure.attach(cleaned_name, 'Очищенное имя отправителя')  # Логируем очищенное имя
        return cleaned_name



    @allure.step('Получение адреса отправителя')
    def get_sender_mailbox(self):

        """Получаем адрес отправителя"""

        sender_mail = parseaddr(self.msg['From'])[1]
        allure.attach(sender_mail, 'Адрес отправителя')  # Логируем адрес отправителя
        return sender_mail



    @allure.step('Получение темы сообщения')
    def get_mail_subject(self):

        """Декодируем заголовок "Тема"."""

        subject = decode_header(self.msg['Subject'])[0][0]
        allure.attach(str(subject), 'Исходная тема сообщения')  # Логируем исходную тему

        if isinstance(subject, bytes):
            subject = subject.decode()

        allure.attach(subject, 'Декодированная тема сообщения')  # Логируем декодированную тему
        return subject



    @allure.step('Получение тела сообщения')
    def get_message_body(self):

        """Декодируем тело сообщения"""

        if self.msg.is_multipart():
            for part in self.msg.walk():
                # Если часть - текстовая
                if part.get_content_type() == "text/plain":
                    self.body = part.get_payload(decode=True).decode()
                    allure.attach(self.body, 'Тело сообщения (многочастное)')  # Логируем тело сообщения
                    break  # Выходим из цикла после первого текстового содержимого
            return self.body
        else:
            # Если сообщение не многочастное
            self.body = self.msg.get_payload(decode=True).decode()
            allure.attach(self.body, 'Тело сообщения (одночастное)')  # Логируем тело сообщения
            return self.body



    # сыровато, дорабатывать
    # def extract_message_body(self, data):
    #     text = BeautifulSoup(data, 'html.parser')
    #     # url = text.find('a')['href'] if text.find('a') else None
    #     text = text.get_text(strip=True)
    #     return text



    @allure.step('Поиск ссылок в теле сообщения')
    def find_url_in_message(self):

        """Находим ссылки в теле сообщения, очищаем их и делаем переход по ним"""

        urls = re.findall(r'https://[^\s<>"]+', self.body)
        cleaned_urls = [url.rstrip('"\'>)') for url in urls]

        allure.attach(str(cleaned_urls), 'Найденные ссылки')  # Логируем найденные ссылки

        if cleaned_urls:
            for url in cleaned_urls:
                allure.attach(url, 'Переход по ссылке')  # Логируем каждую ссылку перед переходом
                Browser(url)



    @ allure.step('Получение времени сообщения')
    def get_time_message(self):

        """Получаем время сообщения"""

        date = self.msg['Date']
        message_time = parsedate_to_datetime(date)

        allure.attach(str(message_time), 'Время сообщения')  # Логируем время сообщения
        return message_time


