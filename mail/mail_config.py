import os
from dotenv import load_dotenv

"""   
ДЛЯ ИНФОРМАЦИИ
yandex_smtp = ['smtp.yandex.ru', 465]   у Яндекс если SSL то 465 порт, если TLS то 587
Адрес почтового сервера — smtp.yandex.ru. Защита соединения — SSL. Порт — 465. Если почтовый клиент начинает соединение без шифрования — 587
mail_smtp = ['smtp.mail.ru', 465]
"""


class MailConfig:


    def __init__(self, name):

        self.name = name
        self.mail = ''
        self.password = ''
        self.smtp_server = ''
        self.smtp_port = ''
        self.set_config()


    def set_config(self):

        load_dotenv()

        config = {
            'slaba': {
                'mail' : os.getenv('slaba_mailbox'),
                'password' : os.getenv('slaba_password'),
                'smtp_server' : os.getenv('slaba_smtp_server'),
                'smtp_port' : os.getenv('slaba_smtp_port')
            },
            'laba87-test1': {
                'mail' : os.getenv('laba87_test1_mailbox'),
                'password' : os.getenv('laba87_test1_password'),
                'smtp_server' : os.getenv('laba87_test1_smtp_server'),
                'smtp_port' : os.getenv('laba87_test1_smtp_port')
            },
            'laba87-test2': {
                'mail': '',
                'password': '',
                'smtp_server': '',
                'smtp_port': ''
            },
        }

        if self.name in config:
            mail_config = config[self.name]
            self.mail = mail_config['mail']
            self.password = mail_config['password']
            self.smtp_server = mail_config['smtp_server']
            self.smtp_port = mail_config['smtp_port']
        else:
            raise ValueError('Указана неверная конфигурация почты, проверьте правильность ввода и наличие конфигурации для указанного адреса.')


    def get_config(self):
        return {
            'mail' : self.mail,
            'password' : self.password,
            'smtp_server' : self.smtp_server,
            'smtp_port' : self.smtp_port
        }


