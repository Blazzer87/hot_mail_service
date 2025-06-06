import email
import imaplib
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import allure
import openpyxl

from mail.database import Database
from mail.mail_message import MailMessage
from mail.mailbox_config import MailConfig






class Mailbox:

    mailbox : MailConfig


    def __init__(self, mailbox):
        self.mailbox = MailConfig(mailbox)
        self.database = None
        self.last_email_id = None
        self.reply_subject = None
        self.message = None


    def get_mail(self, filter_criteria):

        """функция получает почту по протоколу аймап,
        ищет в папке входящих, через filter_criteria - задаётся условие поиска, UNSEEN например - все непрочитанные
        далее берет это сообщение и поочерёдно декодирует имя отправителя, адрес отправителя, тему письма и тело письма
        если в теле письма обнаруживаются ссылки то автоматически происходит их вызов через селениум"""

        with allure.step('Создаём объект IMAP4_SSL для чтения почты'):
            mail = imaplib.IMAP4_SSL("imap.mail.ru")  # подключаемся к серверу

        try:
            mail.login(self.mailbox.mail, self.mailbox.password)  # логинимся

            result, folders = mail.list()
            for folder in folders:
                print(folder)

            mail.select('&BCEEPwQwBDw-')  # выбираем папку, которую будем проверять

            xxx = mail.search(None, filter_criteria)
            print('это тип объекта xxx ', type(xxx))
            print('это объект xxx ', xxx)
            messages = mail.search(None, filter_criteria)[1]


            print('это тип объекта messages ', type(messages))
            print('это длинна  объекта messages ', len(messages))
            print('это объект messages[0]',messages[0])
            print('это объект messages ', messages)

            mail_ids = messages[0].split()

            print('это тип объекта mail_ids ', type(mail_ids))
            print('это объект mail_ids ', mail_ids)


            # Получаем последнее письмо
            if mail_ids:

                self.last_email_id = mail_ids[-1]



                msg_data = mail.fetch(self.last_email_id, '(RFC822)')[1]

                # print('это тип объекта status ', type(status))
                # print('это объект status ', status)

                print('это тип объекта msg_data ', type(msg_data))
                print('это объект msg_data ', msg_data)


                # msg = email.message_from_bytes(msg_data[0][1])
                #
                #
                # self.message = MailMessage(msg)
                #
                #
                # sender_mail = self.message.get_sender_mailbox()
                #
                #
                # subject = self.message.get_mail_subject()
                #
                #
                # body = self.message.get_message_body()
                #
                #
                # message_time, message_time_for_allure = self.message.get_time_message()
                #
                #
                # print("Получено новое сообщение!")
                # print(f'От: {sender_mail}, Тема: {subject}')
                # print(message_time)
                # print(body)
                #
                # return sender_mail, subject, body, message_time

        except Exception as e:
            with allure.step('Обработка ошибки'):
                print("Ошибка функции get_mail:", e)
                allure.attach(str(e), 'Ошибка функции get_mail')  # Логируем текст ошибки

        finally:
            with allure.step('Выходим из почтового ящика'):
                mail.logout()


box = Mailbox('slaba')
box.get_mail('ALL')