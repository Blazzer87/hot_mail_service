import email
import imaplib
import os
import re
import smtplib
import time
from email.header import decode_header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr

from selenium import webdriver

from dotenv import load_dotenv


class Mail:


    yandex_smtp = ['smtp.yandex.ru', 465]
    mail_smtp = ['smtp.mail.ru', 465]
    reply_subject = None


    def __init__(self):

        load_dotenv()

        self.laba_qpdev_credential = {
            'mail': os.getenv('MAIL_LABA_LOGIN'),
            'password': os.getenv('MAIL_LABA_PASSWORD'),
            'password_IDE': os.getenv('MAIL_LABA_PASSWORD_IDE')
        }

        self.laba87_test1_yandex_credential = {
            'mail': os.getenv('YANDEX_LOGIN'),
            'password_IDE': os.getenv('YANDEX_PASSWORD_IDE')
        }



    def send_mail(self, recipient, subject, message_body, smtp_options):

        message = MIMEMultipart()           # создали объект сообщения
        message['From'] = self.laba87_test1_yandex_credential['mail']
        message['To'] = recipient                # кому
        message['Subject'] = subject        # тема сообщения

        message.attach(MIMEText(message_body, 'plain'))     # в объект сообщения мы передаём сообщение,
        # обозначив что его формат будет plain, и это сообщение будет экземпляром класса MIMEText

        try:
            connect = smtplib.SMTP_SSL(*smtp_options)
            # connect.starttls()        используется только с smtplib.SMTP, для незащищенного соединения, которое затем переводится в защищенное.
            connect.login(user = self.laba87_test1_yandex_credential['mail'], password = self.laba87_test1_yandex_credential['password_IDE'])
            connect.send_message(msg = message)
            connect.quit()
        except Exception as e:
            print("Ошибка отправки сообщения", e)



    def get_mail(self, filter_criteria):

        mail = imaplib.IMAP4_SSL("imap.mail.ru")  # подключаемся к серверу
        try:
            mail.login(self.laba_qpdev_credential['mail'], self.laba_qpdev_credential['password_IDE'])  # логинимся
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
                sender_name = self.extract_sender_name(sender_name)

                # Получаем адрес отправителя
                sender_email = parseaddr(msg['From'])[1]

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

                    urls = re.findall(r'https://[^\s<>"]+', body)
                    cleaned_urls = [url.rstrip('"\'>)') for url in urls]
                    if cleaned_urls:
                        print("Найденные ссылки в письме:")
                        for url in cleaned_urls:
                            print(url)
                            options = webdriver.ChromeOptions()
                            options.page_load_strategy = 'eager'
                            driver = webdriver.Chrome(options = options)
                            driver.get(url)
                            time.sleep(2)
                            driver.quit()

                    print("Получено новое сообщение!")
                    print(f'От: {sender_email}, Тема: {subject}')
                    print(body)
                    print("\n")

                    return sender_email, subject, body

        except Exception as e:
            print("Ошибка:", e)

        finally:
            mail.logout()


    def reply_mail(self, recipient, reply_subject, message):

        self.reply_subject = f"Re: {reply_subject}"
        self.message = self.body_message(input_message = message)
        self.send_mail(recipient = recipient,
                       subject = self.reply_subject,
                       message_body = self.message,
                       smtp_options = self.yandex_smtp)
        print(f"Ответное сообщение успешно отправлено - {self.message}")
        print("\n")


    def body_message(self, input_message):

        if "погода" in input_message:
            body_message = "Да, погода сегодня огонь, погнали завтра на речку?"
            return body_message
        else:
            body_message = "Да, большое спасибо Вам за информацию!"
            return body_message


    def extract_sender_name(self, from_header: str) -> str:

        match = re.search(r'<([^>]+)>', from_header)
        if match:
            return match.group(1)
        return from_header.strip()