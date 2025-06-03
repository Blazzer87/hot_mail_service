import random
import time
import allure
import pytz
from datetime import datetime, timedelta
from config import get_config_timeout
from mail.accept_mail_list import accept_mail_list
from mail.mailbox_action import Mailbox


def test_auto_reply(mailbox='slaba'):
    mail_client = Mailbox(mailbox)

    while True:
        with allure.step('Получение непрочитанных писем'):
            unread_email = mail_client.get_mail('(UNSEEN)')

            """если объект входящего непрочитанного письма не None значит есть факт входящего сообщения"""
            if unread_email:

                """получаем из входящего сообщения отправителя, тему письма и тело письма"""
                sender, subject, body, message_time = unread_email

                """ПИСЬМО ПОСТОРОНЕННГО ЯЩИКА НЕ ЧИТАТЬ!!!"""

                with allure.step(f'Обработка письма от {sender} с темой "{subject}"'):
                    allure.attach(body, 'Тело письма')  # Логируем тело письма

                    """проверяем что отправитель письма присутствует в разрешённом для авто-переписки списке"""
                    if sender in accept_mail_list:

                        """определяем текущее дату и время с учётом часового пояса чтобы сравнивать "сравнимое" """
                        current_time = datetime.now(pytz.timezone('Europe/Moscow'))

                        with allure.step('Проверка времени получения письма'):
                            time_difference = current_time - message_time
                            allure.attach(str(time_difference), 'Разница во времени')  # Логируем разницу во времени

                            """если с момент получения сообщения прошло больше минут чем определено в случайном диапазоне из аргументов
                            то происходит отправка сообщения"""
                            if time_difference > timedelta(minutes=random.randrange(*get_config_timeout(mailbox))):

                                with allure.step('Отправка ответного письма'):

                                    """отправляем ответное письмо функция reply_mail под капотом запускает функции:
                                    1) generate_body_message - анализа входящего тела сообщения на наличие маркерных слов и генерации ответного сообщения
                                    2) send_mail - отправки ответного сообщения
                                    3) добавления к теме письма "Re" """
                                    mail_client.open_url_from_message()
                                    mail_client.reply_mail(sender, subject, body)
                                    allure.attach(f'Ответ отправлен отправителю {sender}', 'Статус отправки')
                            else:

                                with allure.step('Пометка письма как непрочитанного'):

                                    """если с момент получения сообщения прошло меньше минут чем определено в случайном диапазоне из аргументов
                                    то происходит сообщение помечается как непрочитанное для следующей проверки"""
                                    mail_client.mark_mail_as_unread()
                                    allure.attach(f'Письмо от {sender} помечено как непрочитанное', 'Статус пометки')

                    else:
                        print(f"Обнаружено непрочитанное письмо, отправитель {sender} отсутствует в accept_mail_list, ответ не отправлен.")
                        allure.attach(f'Ответ не отправлен: {sender} отсутствует в списке разрешенных', 'Статус ответа')

        """тут задаётся таймаут проверки наличия непрочитанных входящих"""
        time.sleep(10)
