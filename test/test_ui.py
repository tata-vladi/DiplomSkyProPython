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


def test_login_button(driver):
   driver.get("https://www.kinopoisk.ru/")

   login_button = driver.find_element(By.CSS_SELECTOR, 'button[class*="styles_loginButton"]')
   login_button.click()
   WebDriverWait(driver, 10).until(
       EC.presence_of_element_located((By.CLASS_NAME, 'passp-add-account-page-title'))
   )
   assert "https://passport.yandex.ru/" in driver.current_url

def test_search_input(driver):
    driver.get("https://www.kinopoisk.ru/")

    driver.find_element(By.NAME, 'kp_query').send_keys('Матрица')

    suggestion_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'suggest-item-film-301'))
    )
    assert suggestion_box.is_displayed()

def test_online_movies_navigation(driver):
    driver.get("https://www.kinopoisk.ru/")
    wait = WebDriverWait(driver, 10)
    elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href="https://hd.kinopoisk.ru/"]')))
    elements[1].click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'h1'))
    )
    assert "https://hd.kinopoisk.ru/" in driver.current_url

def test_watch_movie_button(driver):
    driver.get("https://www.kinopoisk.ru/")
    wait = WebDriverWait(driver, 10)
    elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[contains(text(), "Билеты в кино")]')))
    elements[1].click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'h1'))
    )
    assert "https://www.kinopoisk.ru/lists/movies/movies-in-cinema/" in driver.current_url

def test_play_film(driver):

    driver.get("https://www.kinopoisk.ru/")

    driver.find_element(By.NAME, 'kp_query').send_keys('отверженные')

    suggestion_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'suggest-item-film-566055'))
    )
    assert suggestion_box.is_displayed()