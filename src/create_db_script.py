"""Скрипт для первоначального создания БД и ее таблиц"""
import psycopg2
from psycopg2 import errors
from config import DB_NAME, config_db


def create_db(db_name: str, params: dict):
    conn = psycopg2.connect(dbname="postgres", **params)
    cursor = conn.cursor()
    conn.autocommit = True
    sql = f"CREATE DATABASE {db_name}"
    try:
        cursor.execute(sql)
        print(f"База данных {db_name} успешно создана")
    except errors.DuplicateDatabase:
        print(f"База данных {db_name} уже существует")
    finally:
        cursor.close()
        conn.close()


def execute_sql_script(script_file: str, params: dict) -> None:
    """Выполняет скрипт из файла для создания таблиц и связей в БД."""
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                with open(script_file, 'r', encoding='UTF-8') as file:
                    sql_file = file.read()
                    cur.execute(sql_file)
                print(f"БД {db_name} успешно заполнена")
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()




def main():
    params = config_db()
    # Создание базы данных
    create_db(db_name=DB_NAME, params=params)
    params.update({'dbname': DB_NAME})
    # Создание таблиц


if __name__ == "__main__":
    main()
