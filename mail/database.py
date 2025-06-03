import random
from typing import List

import psycopg2


class Database:


    def __init__(self):

        self.database = "postgres"
        self.host = "192.168.100.200"
        self.user = "postgres"
        self.password = "123"
        self.port = "5432"

        self.db = None
        self.cursor = None
        self.words_list = []

        self.db_connect()



    def db_connect(self):
        try:
            db = psycopg2.connect(database=self.database,
                                          host=self.host,
                                          user=self.user,
                                          password=self.password,
                                          port=self.port)
            self.cursor = db.cursor()

        except Exception as error:
            print("Ошибка в функции db_connect:", error)


    def get_list_with_marker_words(self) -> List:
        self.cursor.execute('SELECT marker_words FROM themes')
        row = self.cursor.fetchall()
        self.words_list = []
        for item in row:
            words = item[0].split(', ')
            self.words_list.extend(words)
        return self.words_list


    def get_themes_id_by_marker_with_priority(self, marker_list):
        conditions = ' OR '.join(['marker_words ILIKE %s' for i in marker_list])
        query = f'''
                SELECT theme_id
                FROM themes
                WHERE {conditions}
                ORDER BY priority ASC
                LIMIT 1
            '''
        params = ['%' + marker + '%' for marker in marker_list]
        self.cursor.execute(query, params)
        theme_id: int = self.cursor.fetchall()[0][0]
        return theme_id


    def get_random_answer_by_themes_id(self, marker_list):
        theme_id = self.get_themes_id_by_marker_with_priority(marker_list)
        self.cursor.execute(f'SELECT answer FROM answers WHERE theme_id = {theme_id}')
        row = self.cursor.fetchall()
        x = len(row)
        random_answer = str(row[random.randrange(0,x)][0])
        return random_answer


    def close_connect(self):
        if self.db:
            self.cursor.close()
            self.db.close()
            print("Соединение закрыто")



