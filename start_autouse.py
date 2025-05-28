import time

from mail.accept_mail_list import accept_mail_list
from mail.mail_action import Mail


def test_auto_reply(mailbox = 'slaba'):

    mail_client = Mail(mailbox)

    while True:
        unread_email = mail_client.get_mail('(UNSEEN)')

        """если объект входящего непрочитанного письма не None значит есть факт входящего сообщения"""
        if unread_email:

            """получаем из входящего сообщения отправителя, тему письма и тело письма"""
            sender, subject, body = unread_email

            """проверяем что отправитель письма присутствует в разрешённом для авто-переписки списке"""
            if sender in accept_mail_list:

                """отправляем ответное письмо
                функция reply_mail под капотом запускает функции:
                1) generate_body_message - анализа входящего тела сообщения на наличие маркерных слов и генерации ответного сообщения
                2) send_mail - отправки ответного сообщения
                3) добавления к теме письма "Re" """
                mail_client.reply_mail(sender, subject, body)
            else:
                print(f"Обнаружено непрочитанное письмо, отправитель {sender} отсутствует в accept_mail_list, ответ не отправлен.")
        time.sleep(10)


min_timeout_sec = 3
max_timeout = 30