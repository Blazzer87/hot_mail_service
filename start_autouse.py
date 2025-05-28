import random
import time
import pytz
from datetime import datetime, timedelta

from mail.accept_mail_list import accept_mail_list
from mail.mailbox_action import Mailbox


def test_auto_reply(mailbox = 'slaba', min_timeout_min = 4, max_timeout_min = 5 ):

    mail_client = Mailbox(mailbox)

    while True:
        unread_email = mail_client.get_mail('(UNSEEN)')

        """если объект входящего непрочитанного письма не None значит есть факт входящего сообщения"""
        if unread_email:

            """получаем из входящего сообщения отправителя, тему письма и тело письма"""
            sender, subject, body, message_time = unread_email

            """проверяем что отправитель письма присутствует в разрешённом для авто-переписки списке"""
            if sender in accept_mail_list:

                """определяем текущее дату и время с учётом часового пояса чтобы сравнивать "сравнимое" """
                current_time = datetime.now(pytz.timezone('Europe/Moscow'))

                """если с момент получения сообщения прошло больше минут чем определено в случайном диапазоне из аргументов
                то происходит отправка сообщения"""
                if current_time > (message_time + timedelta(minutes=(random.randrange(min_timeout_min, max_timeout_min)))):

                    """отправляем ответное письмо функция reply_mail под капотом запускает функции:
                    1) generate_body_message - анализа входящего тела сообщения на наличие маркерных слов и генерации ответного сообщения
                    2) send_mail - отправки ответного сообщения
                    3) добавления к теме письма "Re" """
                    mail_client.reply_mail(sender, subject, body)

                else:
                    """если с момент получения сообщения прошло меньше минут чем определено в случайном диапазоне из аргументов
                    то происходит сообщение помечается как непрочитанное для следующей проверки"""
                    mail_client.mark_mail_as_unread()

            else:
                print(f"Обнаружено непрочитанное письмо, отправитель {sender} отсутствует в accept_mail_list, ответ не отправлен.")

        """тут отпределяется таймаут проверки наличия непрочитанных входящих"""
        time.sleep(10)