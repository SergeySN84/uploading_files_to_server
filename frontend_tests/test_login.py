import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="session")
def browser():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture
def login_page(browser):
    browser.get("http://localhost:8000/admin/")
    return browser


def test_login_success(login_page):
    wait = WebDriverWait(login_page, 20)

    # Вводим логин и пароль
    username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    password_input = login_page.find_element(By.NAME, "password")
    submit_button = login_page.find_element(By.XPATH, "//input[@type='submit']")

    username_input.send_keys("admin_user")
    password_input.send_keys("password123")
    submit_button.click()

    wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))

    logout_link = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#user-tools a"))
    )
    assert logout_link.is_displayed()
