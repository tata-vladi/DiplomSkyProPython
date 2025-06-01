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

def test_search_movie(api_session):
    endpoint = '/v1.4/movie/search'
    query_params = {'query': 'Холоп'}
    full_url = BASE_URL + endpoint

    response = api_session.get(full_url, params=query_params)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, f"Неверный статус-код: {response.status_code}, сообщение: {response.text}"

    data = response.json()

    # Проверяем, что нашлось хотя бы одно совпадающее название
    found = False
    for movie in data['docs']:
        if 'Холоп' in movie['name']:
            found = True
            break

    assert found, "Фильм 'Холоп' не найден в результатах."



def test_get_possible_countries(api_session):
    endpoint = '/v1/movie/possible-values-by-field'
    query_params = {'field': 'countries.name'}  # Параметр field указывает поле countries.name
    full_url = BASE_URL + endpoint

    response = api_session.get(full_url, params=query_params)
    assert response.status_code == 200, f"Неверный статус-код: {response.status_code}, сообщение: {response.text}"

    data = response.json()
    assert isinstance(data, list), "Отсутствует список в ответе"

    # Проверяем, что в списке хотя бы одна страна присутствует
    assert len(data) > 0, "Список стран пуст!"


def test_search_person(api_session):
    endpoint = '/v1.4/person/search'
    query_params = {'query': 'Юра Борисов'}
    full_url = BASE_URL + endpoint

    response = api_session.get(full_url, params=query_params)
    assert response.status_code == 200, f"Неверный статус-код: {response.status_code}, сообщение: {response.text}"

    data = response.json()
    found = False
    for person in data['docs']:
        if 'Юра Борисов' in person['name']:
            found = True
            break

    assert found, "Актер 'Юра Борисов' не найден в результатах."


def test_awards_filter_by_year_and_nomination(api_session):
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
    assert response.status_code == 200, f"Неверный статус-код: {response.status_code}, сообщение: {response.text}"


def test_search_movie_negative():
    endpoint = '/v1.4/movie/search'
    query_params = {'query': 'Холоп'}
    full_url = BASE_URL + endpoint

    response = requests.get(full_url, params=query_params)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 401, f"Неверный статус-код: {response.status_code}, сообщение: {response.text}"




