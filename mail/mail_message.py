import email
import re
from email.header import decode_header
from email.utils import parseaddr, parsedate_to_datetime
from bs4 import BeautifulSoup

from mail.browser import Browser


class MailMessage:

    msg: email.message.Message


    def __init__(self, msg: email.message.Message):
        self.msg = msg
        self.body = None


    def get_sender_name(self):

        """Декодируем заголовок "От" и получаем имя отправителя"""

        sender_name = decode_header(self.msg['From'])[0][0]
        if isinstance(sender_name, bytes):
            sender_name = sender_name.decode()
        sender_name = self.extract_sender_name(sender_name)
        return sender_name


    def extract_sender_name(self, sender_name):

        """вспомогательная функция "извлекатель" - получает имя отправителя очищаяя от лишнего"""

        match = re.search(r'<([^>]+)>', sender_name)
        if match:
            return match.group(1)
        return sender_name.strip()


    def get_sender_mailbox(self):

        """Получаем адрес отправителя"""

        sender_mail = parseaddr(self.msg['From'])[1]
        return sender_mail


    def get_mail_subject(self):

        """Декодируем заголовок "Тема"""

        subject = decode_header(self.msg['Subject'])[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode()
        return subject


    def get_message_body(self):

        """Декодируем тело сообщения"""

        if self.msg.is_multipart():
            for part in self.msg.walk():
                # Если часть - текстовая
                if part.get_content_type() == "text/plain":
                    self.body = part.get_payload(decode=True).decode()
                    break  # Выходим из цикла после первого текстового содержимого
                # self.body = self.extract_message_body(self.body) сыровато, дорабатывать
                return self.body
        else:
            # Если сообщение не многочастное
            self.body= self.msg.get_payload(decode=True).decode()
            # self.body = self.extract_message_body(self.body) сыровато, дорабатывать
            return self.body

    # сыровато, дорабатывать
    # def extract_message_body(self, data):
    #     text = BeautifulSoup(data, 'html.parser')
    #     # url = text.find('a')['href'] if text.find('a') else None
    #     text = text.get_text(strip=True)
    #     return text


    def find_url_in_message(self):

        """Находим ссылки в теле сообщения, очищаем их и делаем переход по ним"""

        urls = re.findall(r'https://[^\s<>"]+', self.body)
        cleaned_urls = [url.rstrip('"\'>)') for url in urls]
        if cleaned_urls:
            for url in cleaned_urls:
                Browser(url)

    def get_time_message(self):
        date = self.msg['Date']
        message_time = parsedate_to_datetime(date)
        return message_time

