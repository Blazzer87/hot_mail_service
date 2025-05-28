import email
import imaplib
import re
import time
from datetime import datetime, timedelta
from email.header import decode_header
from email.utils import parseaddr
from email.utils import parsedate
from email.utils import parsedate_tz
from email.utils import parsedate_to_datetime

import pytz
from selenium import webdriver


def extract_sender_name(from_header: str) -> str:
    """вспомогательная функция "извлекатель" - получает имя отправителя очищаяя от лишнего"""

    match = re.search(r'<([^>]+)>', from_header)
    if match:
        return match.group(1)
    return from_header.strip()


def get_mail(filter_criteria):
    """функция получает почту по протоколу аймап,
    ищет в папке входящих, через filter_criteria - задаётся условие поиска, UNSEEN например - все непрочитанные
    далее берет это сообщение и поочерёдно декодирует имя отправителя, адрес отправителя, тему письма и тело письма
    если в теле письма обнаруживаются ссылки то автоматически происходит их вызов через селениум"""

    mail = imaplib.IMAP4_SSL("imap.mail.ru")  # подключаемся к серверу
    try:
        mail.login('s.laba@qpdev.ru', 'vLuxBLs7Bh23ekSziqq8')  # логинимся
        mail.select('inbox')  # выбираем папку, которую будем проверять

        status, messages = mail.search(None, filter_criteria)
        mail_ids = messages[0].split()

        # Получаем последнее письмо
        if mail_ids:
            last_email_id = mail_ids[-1]
            status, msg_data = mail.fetch(last_email_id, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])

            # Декодируем заголовок "От" и получаем имя отправителя
            sender_name = decode_header(msg['From'])[0][0]
            if isinstance(sender_name, bytes):
                sender_name = sender_name.decode()
            sender_name = extract_sender_name(sender_name)

            # Получаем адрес отправителя
            sender_email = parseaddr(msg['From'])[1]

            # Получаем время
            date = msg['Date']
            message_time = parsedate_to_datetime(date)




            # Декодируем заголовок "Тема"
            subject = decode_header(msg['Subject'])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()

                # Декодируем тело сообщения
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        # Если часть - текстовая
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            break  # Выходим из цикла после первого текстового содержимого
                else:
                    # Если сообщение не многочастное
                    body = msg.get_payload(decode=True).decode()

                # Находим ссылки в теле сообщения, очищаем их и делаем переход по ним
                # urls = re.findall(r'https://[^\s<>"]+', body)
                # cleaned_urls = [url.rstrip('"\'>)') for url in urls]
                # if cleaned_urls:
                #     print("Найденные ссылки в письме:")
                #     for url in cleaned_urls:
                #         print(url)
                #         options = webdriver.ChromeOptions()
                #         options.page_load_strategy = 'eager'
                #         driver = webdriver.Chrome(options=options)
                #         driver.get(url)
                #         time.sleep(2)
                #         driver.quit()

                # print("Получено новое сообщение!")
                # print(f'От: {sender_email}, Тема: {subject}')
                # print(body)
                # print("\n")

                return (
                    # sender_email,
                    # subject,
                    # body,
                    message_time + timedelta(minutes=30)
                )

    except Exception as e:
        print("Ошибка:", e)

    finally:
        mail.logout()


print(get_mail('(UNSEEN)'))




