from api_hh import HeadHunter
from db_manager import DBManager
from pprint import pprint


def main():
    emp_names = input("Введите названия работодателей, вакансии которых "
                      "вы хотите получить, через запятую: \n")

    hh = HeadHunter(emp_names.split(sep=','))
    print('Получаем данные о работодателях...')
    hh.get_employers()
    print(f'Найдено {len(hh.employers)} работодателей')

    # Получение вакансий и запись в БД
    with DBManager() as db:
        db.insert_to_db(table_name='employers', variables=hh.employers)
        n = 1
        for employer in hh.employers:
            print(f'\n{n}: Получаем список вакансий у {employer["name"]}...')
            vacancies = hh.get_vacancies(employer_id=employer['employer_id'])
            db.insert_to_db(table_name='vacancies', variables=vacancies)
            n += 1

    # Работа с полученными вакансиями
    with DBManager() as db:
        while True:
            choice = input("\nВведите:\n"
                           "1 - для получения списка всех компаний и количества вакансий у каждой компании\n"
                           "2 - для получения списка всех вакансий с указанием названия компании, названия вакансии, "
                           "зарплаты и ссылки на вакансию\n"
                           "3 - для получения средней зарплаты по вакансиям\n"
                           "4 - для получения списка всех вакансий, "
                           "у которых зарплата выше средней по всем вакансиям\n"
                           "5 - для поиска, в названии и описании вакансии\n"
                           "quit - для выхода из программы\n")
            if choice == "1":
                pprint(db.get_companies_and_vacancies_count())
                input("Для продолжения нажмите Enter")
                continue
            elif choice == "2":
                pprint(db.get_all_vacancies())
                input("Для продолжения нажмите Enter")
                continue
            elif choice == "3":
                pprint(db.get_avg_salary())
                input("Для продолжения нажмите Enter")
                continue
            elif choice == "4":
                pprint(db.get_vacancies_with_higher_salary())
                input("Для продолжения нажмите Enter")
                continue
            elif choice == "5":
                word = input("Введите слово для поиска\n")
                pprint(db.get_vacancies_with_keyword(word))
                input("Для продолжения нажмите Enter")
                continue
            elif choice.lower() in ("quit", "выход"):
                print("Ждем вас снова!")
                break
            else:
                continue


if __name__ == "__main__":
    main()
