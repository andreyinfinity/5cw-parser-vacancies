"""Скрипт для первоначального создания БД и ее таблиц.
При запуске с уже существующей БД все данные из БД удаляются!"""
import psycopg2
from config import DB_NAME, config_db


def create_db(db_name: str, params: dict):
    conn = psycopg2.connect(dbname="postgres", **params)
    cursor = conn.cursor()
    conn.autocommit = True
    sql = f"CREATE DATABASE {db_name}"
    try:
        cursor.execute(sql)
        print(f"База данных {db_name} успешно создана")
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
    script_file = 'create_db.sql'
    # Создание базы данных
    create_db(db_name=DB_NAME, params=params)
    params.update({'dbname': DB_NAME})
    # Создание таблиц
    execute_sql_script(script_file=script_file, params=params)


if __name__ == "__main__":
    main()
