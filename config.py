import re

import pytest



def get_config_range(mailbox):

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
            min_timeout = timeout_dict.get('min_timeout_min')
            max_timeout = timeout_dict.get('max_timeout_min')
            return min_timeout, max_timeout
        except Exception as e:
            print(f"Ошибка при обработке словаря: {e}")
            return None
    else:
        print(f"Ключ '{mailbox}' не найден в файле.")
        return None