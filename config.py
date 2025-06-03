import json
import re

import allure
import pytest



def get_config_timeout(mailbox):
    with allure.step('Открываем файл конфигурации таймаутов'):
        with open('timeout_config.txt', 'r') as file:
            # Читаем содержимое файла
            content = file.read()

        # ищем нужный словарь
        pattern = rf"{mailbox} = ({{.*?}})"
        match = re.search(pattern, content)

        if match:

            # получаем строку со словарем
            dict_str = match.group(1)

            # перегоняем строку в словарь
            try:
                timeout_dict = eval(dict_str)
                min_timeout: int = timeout_dict.get('min_timeout_min')
                max_timeout: int = timeout_dict.get('max_timeout_min')
                allure.attach(json.dumps(timeout_dict), 'диапазон таймаута успешно определён')
                return min_timeout, max_timeout
            except Exception as e:
                print(f"Ошибка при обработке файла конфигурации: {e}")
                return None
        else:
            print(f"Почтовый ящик '{mailbox}' не найден в конфиге.")
            return None