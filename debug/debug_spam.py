import imaplib
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import allure

from mail.mailbox_config import MailConfig


class Mailbox:

    mailbox : MailConfig


    def __init__(self):
        self.database = None
        self.last_email_id = None
        self.reply_subject = None
        self.message = None


    def find_spam_count(self, recipient_mailbox, sender_mailbox, recipient, subject, message_body):

        recipient_mailbox = MailConfig(recipient_mailbox)

        with allure.step('Создаём объект IMAP4_SSL для чтения почты'):
            mail = imaplib.IMAP4_SSL("imap.mail.ru")  # подключаемся к серверу

        try:
            mail.login(recipient_mailbox.mail, recipient_mailbox.password)  # логинимся
            mail.select('&BCEEPwQwBDw-')
            messages = mail.search(None, '(UNSEEN)')[1]
            mail_ids = messages[0].split()
            spam_count_before_send = len(mail_ids)

            self.send_mail_for_test_durability(sender_mailbox=sender_mailbox,
                                               recipient=recipient,
                                               subject=subject,
                                               message_body=message_body)

            time.sleep(10)

            messages = mail.search(None, '(UNSEEN)')[1]
            mail_ids = messages[0].split()
            spam_count_after_send = len(mail_ids)

            print(f"Было спама - {spam_count_before_send}. Стало спама - {spam_count_after_send}")

        except Exception as e:
            with allure.step('Обработка ошибки'):
                print("Ошибка функции get_mail:", e)
                allure.attach(str(e), 'Ошибка функции find_spam_count')  # Логируем текст ошибки

        finally:
            with allure.step('Выходим из почтового ящика'):
                mail.logout()


    def send_mail_for_test_durability(self, sender_mailbox, recipient, subject, message_body):

        """Функция отправляет почту по протоколу SMTP"""

        sender_mailbox = MailConfig(sender_mailbox)

        message = MIMEMultipart()  # создаем объект сообщения
        message['From'] = self.mailbox.mail
        message['To'] = recipient  # кому
        message['Subject'] = subject  # тема сообщения

        message.attach(MIMEText(message_body, 'plain'))  # добавляем текст сообщения

        try:
            with allure.step('Создаём подключение к SMTP серверу'):
                connect = smtplib.SMTP_SSL(sender_mailbox.smtp_server, sender_mailbox.smtp_port)

            with allure.step('Выполняем логин на SMTP сервере'):
                connect.login(user=sender_mailbox.mail, password=sender_mailbox.password)

            with allure.step('Отправляем сообщение'):
                connect.send_message(msg=message)
                allure.attach(str(message), 'Отправляемое сообщение')  # Логируем отправляемое сообщение
                print(f"Ответное сообщение успешно отправлено - {message_body}")
                print("\n")

        except Exception as e:
            with allure.step('Обработка ошибки отправки сообщения'):
                print("Ошибка отправки сообщения в функции send_mail:", e)
                allure.attach(str(e), 'Ошибка отправки сообщения в функции send_mail_for_test_durability')  # Логируем текст ошибки

        finally:
            with allure.step('Закрываем соединение с SMTP сервером'):
                connect.quit()




box = Mailbox()
box.find_spam_count('s.laba@qpdev.ru','laba87-test1',  'проект тестирования доставляемости', 'Сергей привет, давай проверим тестируемость доставляемости писем')