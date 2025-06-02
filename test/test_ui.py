import allure
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(50)

    yield driver
    driver.quit()

@allure.title("Проверка кнопки авторизации  ")
@allure.description("Тест проверяет работу кнопки авторизации на сайте КиноПоиска.")
def test_login_button(driver):
 with allure.step("Открытие сайта"):
     driver.get("https://www.kinopoisk.ru/")

 with allure.step("Ищем и нажимаем кнопку авторизации"):
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[class*="styles_loginButton"]')
    login_button.click()

 with allure.step("Ждем появления окна авторизации Яндекса"):
     WebDriverWait(driver, 10).until(
       EC.presence_of_element_located((By.CLASS_NAME, 'passp-add-account-page-title'))
   )

 with allure.step("Проверяем перенаправление на страницу Яндекс.Паспорт"):
   assert "https://passport.yandex.ru/" in driver.current_url


@allure.description("Проверка названия в поле поиска и выпадающего списка с предложенными фильмами ")
@allure.title("Проверка заголовка главной страницы")
def test_search_input(driver):
 with allure.step("Переходим на главную страницу КиноПоиска"):
    driver.get("https://www.kinopoisk.ru/")

 with allure.step("Вводим фильм 'Матрица' в поисковое поле"):
    driver.find_element(By.NAME, 'kp_query').send_keys('Матрица')

 with allure.step("Ждем появления блока с предложениями фильмов"):
    suggestion_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'suggest-item-film-301'))
    )
 with allure.step("Проверяем, что блок с предложением отображается"):
    assert suggestion_box.is_displayed()


@allure.title("Проверка перехода на раздел онлайн-кинотеатров")
@allure.description("Тест проверяет переход на сайт HD.Kinopoisk.ru.")
def test_online_movies_navigation(driver):
 with allure.step("Переходим на главную страницу КиноПоиска"):
    driver.get("https://www.kinopoisk.ru/")

 with allure.step("Ищем ссылку на онлайн-фильмы и переходим по ней"):
    wait = WebDriverWait(driver, 10)
    elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href="https://hd.kinopoisk.ru/"]')))
    elements[1].click()

 with allure.step("Проверяем открытие страницы онлайн-кино"):
  WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'h1'))
    )
 assert "https://hd.kinopoisk.ru/" in driver.current_url


@allure.title("Проверка перехода на страницу показов фильмов в кинотеатрах")
@allure.description("Тест проверяет доступность раздела покупки билетов в кино.")
def test_watch_movie_button(driver):
 with allure.step("Переходим на главную страницу КиноПоиска"):
    driver.get("https://www.kinopoisk.ru/")
 with allure.step("Ищем и кликаем на кнопку 'Билеты в кино'"):
    wait = WebDriverWait(driver, 10)
    elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[contains(text(), "Билеты в кино")]')))
    elements[1].click()

 with allure.step("Проверяем переход на нужную страницу"):
     WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'h1'))
    )
     assert "https://www.kinopoisk.ru/lists/movies/movies-in-cinema/" in driver.current_url


@allure.title("Проверка выбора фильма для просмотра")
@allure.description("Тест проверяет процесс выбора фильма для воспроизведения.")
def test_play_film(driver):
 with allure.step("Переходим на главную страницу КиноПоиска"):
    driver.get("https://www.kinopoisk.ru/")

 with allure.step("Вводим название фильма 'Отверженные' в поисковое поле"):
    driver.find_element(By.NAME, 'kp_query').send_keys('отверженные')

 with allure.step("Ждем появления блока с результатами поиска"):
    suggestion_box = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.ID, 'suggest-item-film-566055'))
    )

 with allure.step("Проверяем видимость блока с результатом поиска"):
   assert suggestion_box.is_displayed()