import psycopg2


class DBManager:
    """
    Класс для подключения к базе данных Postgres и работе с вакансиями, содержащимися в ней
    """
    def __init__(self, params):
        """
        Инициазизатор класса
        :param params: параметры для подключения к базе данных
        """
        self.params = params

    @staticmethod
    def get_companies_and_vacancies_count(table_name, cur):
        """
        Получает список всех компаний и количество вакансий у каждой компании
        """
        cur.execute(f'SELECT employer, count(*) FROM {table_name} GROUP BY employer')
        result = cur.fetchall()

        return result

    @staticmethod
    def get_all_vacancies(table_name, cur):
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию.
        """
        cur.execute(f'SELECT * FROM {table_name}')
        result = cur.fetchall()

        return result

    @staticmethod
    def get_avg_salary(table_name, cur):
        """
        Получает среднюю зарплату по вакансиям
        """
        cur.execute(f'SELECT AVG(min_salary) as average_min, '
                    f'AVG(max_salary) as average_max  FROM {table_name}')
        result = cur.fetchall()

        return result

    @staticmethod
    def get_vacancies_with_higher_salary(table_name, cur):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        """
        cur.execute(f'SELECT * FROM {table_name} '
                    f'WHERE min_salary > (SELECT AVG(min_salary) FROM {table_name})')
        result = cur.fetchall()

        return result

    @staticmethod
    def get_vacancies_with_keyword(table_name, keyword, cur):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например 'python'
        """
        cur.execute(f"SELECT * FROM {table_name} "
                    f"WHERE name LIKE '%{keyword}%'")
        result = cur.fetchall()

        return result

    def manager(self, key: str, table_name, keyword=None) -> list[tuple]:
        """
        Метод-менеджер для вызова других методов класса
        :param key: ключ
        :param table_name: название таблицы для обращения
        :param keyword: ключевое слово для фильтрации
        :return: результат работы соответствующего SQL запроса
        """
        conn = None
        try:
            with psycopg2.connect(**self.params) as conn:
                with conn.cursor() as cur:

                    if key == '1':
                        rows = self.get_companies_and_vacancies_count(table_name, cur)

                    elif key == '2':
                        rows = self.get_all_vacancies(table_name, cur)

                    elif key == '3':
                        rows = self.get_avg_salary(table_name, cur)

                    elif key == '4':
                        rows = self.get_vacancies_with_higher_salary(table_name, cur)

                    elif key == '5':
                        rows = self.get_vacancies_with_keyword(table_name, keyword, cur)

        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
            return rows

