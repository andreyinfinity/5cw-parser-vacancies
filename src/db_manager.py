"""Модуль для работы с БД Postgres"""
import psycopg2
from config import config_db, DB_NAME


params = config_db()
params.update({'dbname': DB_NAME})


def insert_to_db(table_name: str, variables: list[dict], db_parameters: [dict]) -> None:
    """Подключение к БД и запись данных в таблицу."""
    ok = 0
    conn = psycopg2.connect(**db_parameters)
    cursor = conn.cursor()
    for var in variables:
        query, values = build_insert_query(table_name, var)
        try:
            cursor.execute(query=query, vars=values)
            conn.commit()
            ok += 1
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
            conn.rollback()
    cursor.close()
    conn.close()
    print(f"Успешно добавлено {ok} из {len(variables)} записей в {table_name}.")


def build_insert_query(table_name: str, variables: dict) -> tuple[str, tuple]:
    """Формирование строки запроса """
    values_num = ', '.join(['%s'] * len(variables))
    column_names = ', '.join(variables.keys())
    values = tuple(variables.values())
    query = f"INSERT INTO {table_name} ({column_names}) VALUES({values_num})"
    return query, values


if __name__ == "__main__":
    # Проверка работы модуля
    out = [{'employer_id': 19, 'name': 'Yandex', 'url': 'http'}, {'employer_id':928,'name':5,'url':6}]
    insert_to_db('employers', out, params)

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
