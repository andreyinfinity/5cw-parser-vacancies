"""
Модуль работы с API hh
"""
import time
import requests
import os.path
# from vacancies import Vacancies
from datetime import datetime
# from abc_classes import AbsAPI


class HeadHunter:
    area_url_api = "https://api.hh.ru/areas"
    vacancy_url_api = "https://api.hh.ru/vacancies"
    employers_url_api = "https://api.hh.ru/employers"

    def __init__(self, area: str, employers: tuple):
        self.area_name: str = area.capitalize()
        self.area_id: int = self.get_area_id()
        self.employers: tuple[str] = employers
        self.emp_info = []
        self.vacancies = []

    def get_areas(self) -> list[dict]:
        """Метод получения общего списка населенных пунктов"""
        return requests.get(self.area_url_api).json()

    def get_area_id(self) -> int:
        """Метод получения id города по его названию. Если город не найден, то возвращается id страны Россия"""
        areas = self.get_areas()
        area_id = self.find_id(areas[0])
        if area_id:
            return int(area_id)
        self.area_name = 'Россия'
        return 113

    def find_id(self, areas: dict, area_id=None) -> str:
        """Метод поиска id города по его названию."""
        if areas['areas']:
            for area in areas['areas']:
                area_id = self.find_id(area, area_id)
                if area_id:
                    break
            return area_id
        else:
            if areas['name'].lower() == self.area_name.lower():
                return areas['id']

    def create_employer_params(self, employer) -> dict:
        """Создание параметров для поиска работодателей. Возвращает словарь с параметрами."""
        params = {
            'text': employer,
            'only_with_vacancies': True,
            'page': 0,
            'per_page': 100
        }
        return params

    def create_vacancy_params(self, employer_id) -> dict:
        """Создание параметров для поиска вакансий. Возвращает словарь с параметрами."""
        params = {
            'employer_id': employer_id,
            'page': 0,
            'per_page': 100
        }
        return params

    def get_employers(self):
        """Текст для поиска. Переданное значение ищется в названии и описании работодателя"""
        for employer in self.employers:
            params = self.create_employer_params(employer=employer)
            response = requests.get(self.employers_url_api, params=params)
            if response.ok:
                self.emp_info.extend(response.json()['items'])

    def get_vacancies(self, employer_id: int):
        """Получение списка вакансий по заданным параметрам."""
        params = self.create_vacancy_params(employer_id)
        pages = 1
        vacancies_list = []
        while params['page'] < pages:
            response = requests.get(self.vacancy_url_api, params=params)
            if response.ok:
                data = response.json()
                params['page'] += 1
                pages = int(data.get('pages'))
                vacancies_list.extend(data.get("items"))
            else:
                break
            time.sleep(0.1)
        return vacancies_list

    # def create_vacancies(self, vac_list: list[dict]) -> list[Vacancies]:
    #     """Метод создания экземпляров класса Вакансии. Возвращает список экземпляров класса."""
    #     all_hh_vacancies = []
    #     for item in vac_list:
    #         v = dict()
    #         v["title"] = item.get("name")
    #         v["area"] = item.get("area").get("name")
    #         v["url"] = item.get("alternate_url")
    #         try:
    #             v["salary"] = int(item.get("salary").get("from"))
    #         except AttributeError:
    #             v["salary"] = 0
    #         except TypeError:
    #             v["salary"] = 0
    #         v["date_published"] = datetime.fromisoformat(item.get("published_at")).strftime("%Y-%m-%d,%H:%M:%S")
    #         try:
    #             v["employer"] = item.get("employer").get("name")
    #         except AttributeError:
    #             v["employer"] = 'не указано'
    #         try:
    #             v["responsibility"] = item.get("snippet").get("responsibility")
    #         except AttributeError:
    #             v["responsibility"] = 'не указано'
    #         v["employment"] = item.get("employment").get("name")
    #         v["experience"] = item.get("experience").get("name")
    #         all_hh_vacancies.append(Vacancies(vacancy=v))
    #     return all_hh_vacancies


if __name__ == "__main__":
    # from files_module import JsonFile
    # from config import HH_AREAS
    from pprint import pprint

    hh = HeadHunter('Казань', ("Яндекс", "ВТБ"))
    hh.get_employers()

    for employer in hh.emp_info:
        pprint(hh.get_vacancies(employer_id=employer['id']))


#     print(hh.area_id, hh.area_name, hh.salary, hh.search_text)
#     hh.get_vacancies()
#
#     # vacancies = Vacancies.vacancies_list
#     # hh_vac_json = JsonFile(HH_VAC)
#     # hh_vac_json.save_to_file(vacancies)
#     # hh_vac_json.add_to_file(vacancies)
#     # pprint(Vacancies.vacancies_list, indent=2)
#     # Vacancies.sort_vacancies_by_date()
#     # pprint(Vacancies.vacancies_list, indent=2)
#     # Vacancies.sort_vacancies_by_date(reverse=True)
#     # pprint(Vacancies.vacancies_list, indent=2)
#     Vacancies.sort_vacancies_by_salary()
#     pprint(Vacancies.vacancies_list, indent=2)
