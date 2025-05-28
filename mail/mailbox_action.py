import email
import imaplib
import os
import re
import smtplib
from email.header import decode_header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr
import openpyxl


from mail.browser import Browser
from mail.mail_message import MailMessage
from mail.mailbox_config import MailConfig


class Mailbox:

    mailbox : MailConfig


    def __init__(self, mailbox):
        self.mailbox = MailConfig(mailbox)
        self.last_email_id = None
        self.reply_subject = None

    def get_mail(self, filter_criteria):

        """функция получает почту по протоколу аймап,
        ищет в папке входящих, через filter_criteria - задаётся условие поиска, UNSEEN например - все непрочитанные
        далее берет это сообщение и поочерёдно декодирует имя отправителя, адрес отправителя, тему письма и тело письма
        если в теле письма обнаруживаются ссылки то автоматически происходит их вызов через селениум"""

        mail = imaplib.IMAP4_SSL("imap.mail.ru")  # подключаемся к серверу
        try:
            mail.login(self.mailbox.mail, self.mailbox.password)  # логинимся
            mail.select('inbox')  # выбираем папку, которую будем проверять

            status, messages = mail.search(None, filter_criteria)
            mail_ids = messages[0].split()

            # Получаем последнее письмо
            if mail_ids:
                self.last_email_id = mail_ids[-1]
                status, msg_data = mail.fetch(self.last_email_id, '(RFC822)')
                msg = email.message_from_bytes(msg_data[0][1])

                message = MailMessage(msg)

                sender_mail = message.get_sender_mailbox()
                subject = message.get_mail_subject()
                body = message.get_message_body()
                message.find_url_in_message()
                message_time = message.get_time_message()

                print("Получено новое сообщение!")
                print(f'От: {sender_mail}, Тема: {subject}')
                print(message_time)
                print(body)

                return sender_mail, subject, body, message_time

        except Exception as e:
            print("Ошибка:", e)

        finally:
            mail.logout()


    def mark_mail_as_unread(self):

        """Функция устанавливает признак 'непрочитано' письму по его айдишнику."""

        mail = imaplib.IMAP4_SSL("imap.mail.ru")  # подключаемся к серверу
        try:
            mail.login(self.mailbox.mail, self.mailbox.password)  # логинимся
            mail.select('inbox')  # выбираем папку, которую будем проверять

            # Устанавливаем флаг 'непрочитано' для письма
            mail.store(self.last_email_id, '-FLAGS', '\Seen')

            print(f"Письмо с ID {self.last_email_id} помечено как непрочитанное.")

        except Exception as e:
            print("Ошибка:", e)

        finally:
            mail.logout()


    def send_mail(self, recipient, subject, message_body):

        """функция отправляет почту по протоколу SMTP"""

        message = MIMEMultipart()           # создали объект сообщения
        message['From'] = self.mailbox.mail
        message['To'] = recipient                # кому
        message['Subject'] = subject        # тема сообщения

        message.attach(MIMEText(message_body, 'plain'))     # в объект сообщения мы передаём сообщение,
        # обозначив что его формат будет plain, и это сообщение будет экземпляром класса MIMEText

        try:
            connect = smtplib.SMTP_SSL(self.mailbox.smtp_server, self.mailbox.smtp_port)
            # connect.starttls()        используется только с smtplib.SMTP, для незащищенного соединения, которое затем переводится в защищенное.
            connect.login(user = self.mailbox.mail, password = self.mailbox.password)
            connect.send_message(msg = message)
            connect.quit()
            print(f"Ответное сообщение успешно отправлено - {self.message}")
            print("\n")
        except Exception as e:
            print("Ошибка отправки сообщения", e)



    def reply_mail(self, sender_mail, reply_subject, message):

        """функция создаёт ответное сообщение, добавляя Re в тему сообщения,
        вызывает функцию генерации тела ответа
        и вызывает функцию отправки сообщения получая отправителя в аргументах"""

        self.reply_subject = f"Re: {reply_subject}"
        self.message = self.generate_body_message(input_message=message)
        self.send_mail(recipient = sender_mail,
                       subject = self.reply_subject,
                       message_body = self.message)


    def generate_body_message(self, input_message: str):

        """функция ходит в иммитатор БД - файл dialog_model ,берет каждое слово из столбца А и ищет его в теле сообщения
        если находит - то возвращает ответ из столбца Б, который соответствует записи поля А"""

        file_path = os.path.join(os.path.dirname(__file__), 'dialog_model.xlsx')
        workbook = openpyxl.load_workbook(file_path)

        sheet = workbook.active
        keywords = []

        for row in sheet.iter_rows(min_row=1, min_col=1, max_col=1, values_only=True):
            if row[0]:  # Проверяем, что значение не пустое
                keywords.append(str(row[0]).strip())
        for i in keywords:
            if i.lower() in input_message.lower():
                index = keywords.index(i)
                answer = []
                for row in sheet.iter_rows(min_row=1, min_col=2, max_col=2, values_only=True):
                    answer.append(str(row[0]).strip())
                return answer[index]

        other_answer = 'Большое спасибо за информацию, в ближайшее время мы свяжемся с Вами'
        return other_answer
