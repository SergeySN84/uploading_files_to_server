import subprocess
import time
import pytest
from selenium import webdriver


@pytest.fixture(scope="session")
def django_server():
    # Запускаем сервер в фоне
    server = subprocess.Popen(
        ["poetry", "run", "python", "manage.py", "runserver"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    time.sleep(3)  # Ждём запуска
    yield
    server.terminate()
    server.wait()


@pytest.fixture
def browser(django_server):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()
