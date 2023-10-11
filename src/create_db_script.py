"""Скрипт для первоначального создания БД и ее таблиц"""
import psycopg2
from psycopg2 import errors
from config import DB_NAME, DB_PWD


tables = [{'name': 'employers',
           'columns': ["employer_id SERIAL PRIMARY KEY",
                       "name VARCHAR(50)",
                       "url VARCHAR"]},
          {'name': 'vacancies',
           'columns': ["vacancy_id SERIAL PRIMARY KEY",
                       "employer_id int REFERENCES employers(employer_id) NOT NULL",
                       "alternate_url varchar NOT NULL",
                       "area varchar(20)",
                       "published_at date NOT NULL",
                       "employment varchar(100)",
                       "experience varchar(100)",
                       "name varchar(100) NOT NULL",
                       "salary_from int",
                       "salary_to int",
                       "requirement varchar",
                       "responsibility varchar"]}]


def create_db():
    conn = psycopg2.connect(dbname="postgres", user="postgres", password=DB_PWD, host="localhost", port=5432)
    cursor = conn.cursor()
    conn.autocommit = True
    # команда для создания базы данных DB_NAME
    sql = f"CREATE DATABASE {DB_NAME}"
    # выполняем код sql
    try:
        cursor.execute(sql)
        print("База данных успешно создана")
    except errors.DuplicateDatabase:
        print("База данных уже существует")
    finally:
        cursor.close()
        conn.close()


def create_table(table_name: str, variables: str):
    conn = psycopg2.connect(dbname=DB_NAME, user="postgres", password=DB_PWD, host="localhost", port=5432)
    cursor = conn.cursor()
    # создаем таблицу
    try:
        cursor.execute(f"CREATE TABLE {table_name} ({variables})")
        # подтверждаем транзакцию
        conn.commit()
        print(f"Таблица {table_name} успешно создана")
    except errors.DuplicateTable:
        print(f"Таблица {table_name} уже существует")
    finally:
        cursor.close()
        conn.close()


def main():
    # Создание базы данных
    create_db()
    # Создание таблиц
    for table in tables:
        variables = ", ".join(table['columns'])
        create_table(table_name=table['name'], variables=variables)


if __name__ == "__main__":
    main()
