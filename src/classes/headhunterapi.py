import requests


class HeadHunterAPI:
    """
    Класс определяющий функционал для работы с api сайта HeadHunter
    """
    URL = 'https://api.hh.ru/vacancies'  # URL для поиска вакансий

    def get_request(self, employer_id, page, per_page: int = 100) -> None:
        """
        Отправка запроса на API
        :param employer_id: id компании работодателя
        :param page: номер страницы
        :param per_page: количество вакансий на одной странице
        :return: json со списком вакансий
        """

        # сортировка по дате
        params = {'employer_id': employer_id,
                  'page': page,
                  'per_page': per_page,
                  'order_by': "publication_time",
                  }
        response = requests.get(self.URL, params=params).json()
        return response['items']

    def get_vacancies(self, employer_id: int, count) -> list[dict]:
        """
        :param employer_id: id компании работодателя, для которой нужно получить список вакансий
        :param count: максимальное количество вакансий(если открытых вакансий больше count, вернется count вакансий)
        :return: список с вакансиями на соответствующей странице
        """
        vacancies = []  # список вакансий
        for page in range(20):
            if len(vacancies) < count:
                self.get_request(employer_id, page)
                if not page:  # выход из цикла в случае отсутствия страницы
                    break
                vacancies.extend(page)
            else:
                break
        return vacancies

    @staticmethod
    def get_employer_id(employer: str) -> list[dict]:
        """
        Метод для получения информации о компании
        :param employer: ключевое слово для поиска компании
        :return: список с компаниями, найденными по переданному в метод ключевому слову
        """
        url = 'https://api.hh.ru/employers'  # URL работодателей
        params = {'text': employer,
                  'only_with_vacancies': True
                  }

        response = requests.get(url, params=params).json()
        return response['items']
