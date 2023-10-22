"""Скрипт для первоначального создания БД и ее таблиц.
При запуске с уже существующей БД все данные из БД удаляются!"""
import psycopg2
from config import config_db


def create_db(params: dict) -> None:
    """Создание БД для проекта"""
    new_db = params.get('dbname')
    sql_query = f"CREATE DATABASE {new_db}"
    params.update({'dbname': "postgres"})
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    conn.autocommit = True
    try:
        cursor.execute(sql_query)
        print(f"База данных {new_db} успешно создана")
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        cursor.close()
        conn.close()


def execute_sql_script(script_file: str, params: dict) -> None:
    """Выполняет скрипт из файла для создания таблиц и связей в БД."""
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    conn.autocommit = True
    try:
        with open(script_file, 'r', encoding='UTF-8') as file:
            sql_file = file.read()
            cur.execute(sql_file)
        print(f"Таблицы в БД {params['dbname']} успешно созданы")
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        cur.close()
        conn.close()


def main():
    params = config_db()
    # Создание базы данных
    create_db(params=params)
    # Создание таблиц
    params = config_db()
    script_file = 'create_db_tables.sql'
    execute_sql_script(script_file=script_file, params=params)


if __name__ == "__main__":
    main()
