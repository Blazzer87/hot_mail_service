import email
import imaplib
import os
import re
import smtplib
import time
from email.header import decode_header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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
            print("Сообщение успешно отправлено")
        except Exception as e:
            print("Ошибка отправки сообщения", e)



    def reply_email(self, recipient, reply_subject):

        self.reply_subject = f"Re: {reply_subject}"
        self.send_mail(recipient = recipient,
                       subject = self.reply_subject,
                       message_body = "Привет, спасибо за информацию!",
                       smtp_options = self.yandex_smtp)



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

                # Декодируем заголовок "От"
                sender = decode_header(msg['From'])[0][0]
                if isinstance(sender, bytes):
                    sender = sender.decode()

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
                            driver = webdriver.Chrome()
                            driver.get(url)
                            time.sleep(5)
                            driver.quit()

                    print(f'От: {sender}, Тема: {subject}')
                    print(body)

                    return sender, subject

        except Exception as e:
            print("Ошибка:", e)

        finally:
            mail.logout()


