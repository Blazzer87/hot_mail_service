import time

def test_auto_reply(mail_client):
    while True:
        unread_email = mail_client.get_mail('(UNSEEN)')
        if unread_email:
            sender, subject = unread_email
            mail_client.reply_email(sender, subject)
        time.sleep(10)
