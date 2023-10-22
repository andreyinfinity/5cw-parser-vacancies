"""Модуль для работы с БД Postgres"""
import psycopg2
from config import config_db


class DBManager:
    def __init__(self):
        self.params = config_db()
        self.conn = None
        self.cur = None

    def __enter__(self):
        self.conn = psycopg2.connect(**self.params)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exception_type, exception_val, trace):
        self.cursor.close()
        self.conn.close()

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """Метод получает список всех компаний и количество вакансий
        у каждой компании."""
        sql = """
            SELECT employers.name, COUNT(*) FROM employers 
            JOIN vacancies USING(employer_id)
            GROUP BY employers.name
            ORDER BY COUNT(*) DESC
        """
        return self.select_from_db(query=sql)

    def get_all_vacancies(self) -> list[tuple]:
        """Метод получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        sql = """
            SELECT employers.name AS employer, vacancies.name AS vacancy, 
            (salary_from + salary_to)/2 AS salary, alternate_url AS url 
            FROM employers
            JOIN vacancies USING(employer_id)
            ORDER BY employers.name
        """
        return self.select_from_db(query=sql)

    def get_avg_salary(self) -> int:
        """Метод получает среднюю зарплату по вакансиям."""
        sql = """
            SELECT AVG((salary_from + salary_to)/2) AS avg_salary 
            FROM vacancies
        """
        return int(self.select_from_db(query=sql)[0][0])

    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """Метод получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        sql = """
            SELECT * FROM vacancies
            WHERE (salary_from + salary_to)/2 > 
            (SELECT AVG((salary_from + salary_to)/2) FROM vacancies)
            ORDER BY salary_from
        """
        return self.select_from_db(query=sql)

    def get_vacancies_with_keyword(self, word: str) -> list[tuple]:
        """Метод получает список всех вакансий, в названии или
        описании которых содержатся переданные в метод слова."""
        sql = f"""
            SELECT * FROM vacancies
            WHERE name ILIKE '%{word}%' or requirement ILIKE '%{word}%'
        """
        return self.select_from_db(query=sql)

    def insert_to_db(self, table_name: str, variables: list[dict]) -> None:
        """Подключение к БД и запись данных в таблицу."""
        ok = 0
        for var in variables:
            query, values = self._build_insert_query(table_name, var)
            try:
                self.cursor.execute(query=query, vars=values)
                self.conn.commit()
                ok += 1
            except(Exception, psycopg2.DatabaseError):
                # print(error)
                self.conn.rollback()
        print(f"Успешно добавлено {ok} из {len(variables)} записей в {table_name}.")

    def _build_insert_query(self, table_name: str, variables: dict) -> tuple[str, tuple]:
        """Формирование строки запроса """
        values_num = ', '.join(['%s'] * len(variables))
        column_names = ', '.join(variables.keys())
        values = tuple(variables.values())
        query = f"INSERT INTO {table_name} ({column_names}) VALUES({values_num})"
        return query, values

    def select_from_db(self, query: str) -> list[tuple]:
        self.cursor.execute(query=query)
        return self.cursor.fetchall()


if __name__ == "__main__":
    from pprint import pprint
    # Проверка работы модуля
    with DBManager() as db:
        pprint(db.get_vacancies_with_keyword('python'))
    # out = [{'employer_id': 19, 'name': 'Yandex', 'url': 'http'}, {'employer_id':928,'name':5,'url':6}]
    # insert_to_db('employers', out)

#
# def select_from_db(table_name: str, column_names: tuple):
#     names = ', '.join(column_names)
#     query = f"SELECT {names} FROM {table_name} WHERE employer_id=4"
#     print(query)
#     conn = psycopg2.connect(dbname=DB_NAME, user="postgres", password=DB_PASS, host="localhost")
#     cursor = conn.cursor()
#     try:
#         cursor.execute(query=query)
#         print(cursor.fetchall())
#     except errors.UniqueViolation:
#         print(f"Ошибка записи в {table_name}, уникальный ключ уже существует.")
#     finally:
#         cursor.close()
#         conn.close()
#
#
# def check_id(table_name: str, column_name: str, value):
#     query = f"SELECT {column_name} FROM {table_name} WHERE {column_name}={value}"
#     print(query)
#     conn = psycopg2.connect(dbname=DB_NAME, user="postgres", password=DB_PASS, host="localhost")
#     cursor = conn.cursor()
#     try:
#         cursor.execute(query=query)
#         print(cursor.fetchone())
#     except errors.UniqueViolation:
#         print(f"Ошибка записи в {table_name}, уникальный ключ уже существует.")
#     finally:
#         cursor.close()
#         conn.close()


# check_id(table_name='employers', column_name="employer_id", value=20)
# insert_to_db(table_name='employers', column_names=("employer_id", "name", "url"), vars_list=[(54, 'Yandex1', 'http://ya.ru'), (8, 'Yandex2', 'http://ya.ru')])
# добавить название таблицы и поля, Val по количеству полей
# query = f"INSERT INTO {table}()"
