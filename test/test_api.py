import allure
import requests
import pytest

API_TOKEN = 'HMFMKEX-SND4R4W-GQGS724-KWT1V2S'
BASE_URL = 'https://api.kinopoisk.dev/'
HEADERS = {
    'X-Api-Key': API_TOKEN,
    'Content-Type': 'application/json',
}

@pytest.fixture(scope="module")
def api_session():
    s = requests.Session()
    s.headers.update(HEADERS)
    yield s

@allure.title("Проверка нахождения фильма 'Холоп'")
@allure.description("Проверяет, что API корректно ищет фильм по заданному запросу.")
def test_search_movie(api_session):
 with allure.step("Отправляем запрос на поиск фильма 'Холоп'"):
    endpoint = '/v1.4/movie/search'
    query_params = {'query': 'Холоп'}
    full_url = BASE_URL + endpoint

    response = api_session.get(full_url, params=query_params)
    print(response.status_code)
    print(response.text)
 with allure.step("Проверяем успешность запроса"):
    assert response.status_code == 200, f"Неверный статус-код: {response.status_code}, сообщение: {response.text}"

 with allure.step("Анализируем результат и ищем фильм 'Холоп'"):
    data = response.json()
    found = False
    for movie in data['docs']:
        if 'Холоп' in movie['name']:
            found = True
            break

    assert found, "Фильм 'Холоп' не найден в результатах."


@allure.title("Проверка доступности списка стран")
@allure.description("Проверяет возможность получения полного списка стран.")
def test_get_possible_countries(api_session):
 with allure.step("Отправляем запрос на получение списка стран"):
    endpoint = '/v1/movie/possible-values-by-field'
    query_params = {'field': 'countries.name'}  # Параметр field указывает поле countries.name
    full_url = BASE_URL + endpoint

    response = api_session.get(full_url, params=query_params)
 with allure.step("Проверяем успешность запроса"):
    assert response.status_code == 200, f"Неверный статус-код: {response.status_code}, сообщение: {response.text}"

 with allure.step("Проверяем, что возвращенный объект является списком"):
    data = response.json()
    assert isinstance(data, list), "Отсутствует список в ответе"

 with allure.step("Проверяем, что список не пустой"):
    assert len(data) > 0, "Список стран пуст!"


@allure.title("Проверка поиска актера 'Юра Борисов'")
@allure.description("Проверяет, что API корректно находит нужного актера.")
def test_search_person(api_session):
 with allure.step("Отправляем запрос на поиск актера 'Юра Борисов'"):
    endpoint = '/v1.4/person/search'
    query_params = {'query': 'Юра Борисов'}
    full_url = BASE_URL + endpoint

    response = api_session.get(full_url, params=query_params)
 with allure.step("Проверяем успешность запроса"):
    assert response.status_code == 200, f"Неверный статус-код: {response.status_code}, сообщение: {response.text}"

 with allure.step("Анализируем результат и ищем актера 'Юра Борисов'"):
    data = response.json()
    found = False
    for person in data['docs']:
        if 'Юра Борисов' in person['name']:
            found = True
            break

    assert found, "Актер 'Юра Борисов' не найден в результатах."


@allure.title("Проверка фильтрации наград 'Оскар' за 2021 год")
@allure.description("Проверяет возможность фильтрации наград по критерию 'Оскар' за определенный год.")
def test_awards_filter_by_year_and_nomination(api_session):
 with allure.step("Отправляем запрос на получение наград с фильтрацией"):
    endpoint = '/v1.4/movie/awards'
    query_params = {
        'selectFields': 'nomination',
        'notNullFields': 'nomination.award.year',
        'sortField': 'nomination.award.year',
        'sortType': '1',  # ASCENDING sort order
        'nomination.title': 'Оскар',
        'nomination.award.year': '2021'
    }
    full_url = BASE_URL + endpoint

    response = api_session.get(full_url, params=query_params)
 with allure.step("Проверяем успешность запроса"):
    assert response.status_code == 200, f"Неверный статус-код: {response.status_code}, сообщение: {response.text}"


@allure.title("Проверка отсутствия токена")
@allure.description("Проверяет поведение API при отсутствии токена аутентификации.")
def test_search_movie_negative():
 with allure.step("Отправляем запрос без заголовков авторизации"):
    endpoint = '/v1.4/movie/search'
    query_params = {'query': 'Холоп'}
    full_url = BASE_URL + endpoint

    response = requests.get(full_url, params=query_params)
    print(response.status_code)
    print(response.text)
 with allure.step("Проверяем ошибку авторизации"):
    assert response.status_code == 401, f"Неверный статус-код: {response.status_code}, сообщение: {response.text}"




