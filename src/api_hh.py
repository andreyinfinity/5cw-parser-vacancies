"""
Модуль работы с API hh
"""
import time
import requests
from datetime import datetime


class HeadHunter:
    _area_url_api = "https://api.hh.ru/areas"
    _vacancy_url_api = "https://api.hh.ru/vacancies"
    _employers_url_api = "https://api.hh.ru/employers"

    def __init__(self, employer_names: list[str]):
        # self.area_name: str = area.capitalize()
        # self.area_id: int = self.get_area_id()
        self._employer_names: list[str] = employer_names
        self.employers = []

    # def get_areas(self) -> list[dict]:
    #     """Метод получения общего списка населенных пунктов"""
    #     return requests.get(self.area_url_api).json()
    #
    # def get_area_id(self) -> int:
    #     """Метод получения id города по его названию. Если город не найден, то возвращается id страны Россия"""
    #     areas = self.get_areas()
    #     area_id = self.find_id(areas[0])
    #     if area_id:
    #         return int(area_id)
    #     self.area_name = 'Россия'
    #     return 113
    #
    # def find_id(self, areas: dict, area_id=None) -> str:
    #     """Метод поиска id города по его названию."""
    #     if areas['areas']:
    #         for area in areas['areas']:
    #             area_id = self.find_id(area, area_id)
    #             if area_id:
    #                 break
    #         return area_id
    #     else:
    #         if areas['name'].lower() == self.area_name.lower():
    #             return areas['id']

    def _create_employer_params(self, emp_name: str) -> dict:
        """Создание параметров для поиска работодателей. Возвращает словарь с параметрами."""
        params = {
            'text': emp_name,
            'only_with_vacancies': True,
            'page': 0,
            'per_page': 100
        }
        return params

    def _create_vacancy_params(self, employer_id) -> dict:
        """Создание параметров для поиска вакансий. Возвращает словарь с параметрами."""
        params = {
            'employer_id': employer_id,
            'page': 0,
            'per_page': 100
        }
        return params

    def get_employers(self) -> None:
        """Получение работодателей по API"""
        for item in self._employer_names:
            params = self._create_employer_params(emp_name=item)
            response = requests.get(self._employers_url_api, params=params)
            if response.ok:
                self._parse_emp_info(response.json()['items'])

    def _parse_emp_info(self, data: list[dict]) -> None:
        """Выборка необходимых полей для employers"""
        for item in data:
            info = {'employer_id': item.get('id'),
                    'name': item.get('name'),
                    'url': item.get('alternate_url')}
            self.employers.append(info)

    def get_vacancies(self, employer_id: int) -> list[dict]:
        """Получение списка вакансий по API."""
        params = self._create_vacancy_params(employer_id)
        pages = 1
        vacancies_list = []
        while params['page'] < pages:
            response = requests.get(self._vacancy_url_api, params=params)
            if response.ok:
                data = response.json()
                params['page'] += 1
                pages = int(data.get('pages'))
                vacancies_list.extend(data.get("items"))
            else:
                break
            time.sleep(0.5)
        return self._parse_vacancies(data=vacancies_list)

    def _parse_vacancies(self, data: list[dict]) -> list[dict]:
        """Получение необходимых полей для таблицы vacancies.
        Если поле 'salary_to' отсутствует, то оно берется из 'salary_from'."""
        vacancies = []
        for item in data:
            v = dict()
            v["vacancy_id"] = item.get("id")
            v["employer_id"] = item.get("employer").get("id")
            v["alternate_url"] = item.get("alternate_url")
            v["area"] = item.get("area").get("name")
            v["published_date"] = datetime.fromisoformat(item.get("published_at")).strftime("%Y-%m-%d,%H:%M:%S")
            v["employment"] = item.get("employment").get("name")
            v["experience"] = item.get("experience").get("name")
            v["name"] = item.get("name")
            try:
                salary_from = int(item.get("salary").get("from"))
            except (AttributeError, TypeError):
                salary_from = None
            v["salary_from"] = salary_from
            try:
                v["salary_to"] = int(item.get("salary").get("to"))
            except (AttributeError, TypeError):
                v["salary_to"] = salary_from
            v["requirement"] = item.get("snippet").get("requirement")
            v["responsibility"] = item.get("snippet").get("responsibility")
            vacancies.append(v)
        return vacancies


if __name__ == "__main__":
    from pprint import pprint

    hh = HeadHunter(["Яндекс", "ВТБ"])
    hh.get_employers()

    for employer in hh.employers:
        pprint(hh.get_vacancies(employer_id=employer['id']))
