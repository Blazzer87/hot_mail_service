import random
import time
import allure
import pytest
import pytz
from datetime import datetime, timedelta
from config import get_config_timeout
from mail.accept_mail_list import accept_mail_list
from mail.mailbox_action import Mailbox



@pytest.mark.parametrize('sender, recipient',
                         [('laba87-test1', 'slaba'),
                          ('laba87-test1', 'test1@qpdev.ru'),
                          ('laba87-test1', 'test2@qpdev.ru')]
                         )
def test_delivery_check(sender, recipient):

    sender_mailbox = Mailbox(sender)
    recipient_mailbox = Mailbox(recipient)

    recipient_mailbox.find_spam_count()

    sender_mailbox.send_mail(recipient=recipient_mailbox.mailbox.mail,
                             subject='завтра важный день',
                             message_body='давай обсудим завтрашнее мероприятие')

    recipient_mailbox.find_spam_count()
