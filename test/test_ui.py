import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="module")
def driver():
    # Запускаем браузер Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(50)

    yield driver
    driver.quit()  # Закрываем браузер после всех тестов

class TestKinopoiskUI:
    def test_login_button(self, driver):
        """Тест №1: Проверка появления формы входа"""
        driver.get("https://www.kinopoisk.ru/")

        login_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="header-auth-button"]')
        login_button.click()

        registration_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="login"]'))
        )
        assert registration_field.is_displayed(), "Форма регистрации не отображается"

    def test_search_input(self, driver):
        """Тест №2: Выполнение поиска фильма и проверка результата"""
        driver.get("https://www.kinopoisk.ru/")

        search_input = driver.find_element(By.CSS_SELECTOR, 'input[type="search"]')
        search_input.send_keys('Матрица')

        suggestion_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'suggestion-box__content'))
        )
        assert suggestion_box.is_displayed(), "Выпадающий список фильмов не появился"

    def test_novelties_navigation(self, driver):
        """Тест №3: Переход на страницу новинок"""
        driver.get("https://www.kinopoisk.ru/")

        novelties_link = driver.find_element(By.XPATH, '//a[@href="/novelty/"]')
        novelties_link.click()

        title = WebDriverWait(driver, 10).until(
            EC.title_contains('Новинки кино онлайн бесплатно и легально | КиноПоиск')
        )
        assert title, "Страница новинок не загружена"

    def test_watch_movie_button(self, driver):
        """Тест №4: Появление кнопки просмотра фильма на странице фильма"""
        driver.get("https://www.kinopoisk.ru/film/matrix/")

        watch_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.player-button'))
        )
        assert watch_button.is_displayed(), "Кнопка 'Смотреть' не отображается"

    def test_play_film(self, driver):
        """Тест №5: Пуск воспроизведения фильма"""
        driver.get("https://www.kinopoisk.ru/film/matrix/watch/")

        play_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.player-control-play'))
        )
        play_button.click()