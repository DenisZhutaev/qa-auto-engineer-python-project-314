import os
import platform

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from tests.pages.labels_page import LabelsPage
from tests.pages.statuses_page import StatusesPage
from tests.pages.tasks_page import TasksPage
from tests.pages.users_page import UsersPage
from tests.support.session import open_dashboard


@pytest.fixture
def base_url():
    if os.getenv("APP_BASE_URL"):
        return os.getenv("APP_BASE_URL")

    if os.path.exists("/.dockerenv"):
        return "http://server"

    return "http://localhost:5173"


@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--remote-debugging-port=9222")

    if platform.system() == "Linux" and os.path.exists("/usr/bin/chromium"):
        chrome_options.binary_location = "/usr/bin/chromium"

    driver_instance = webdriver.Chrome(options=chrome_options)
    driver_instance.implicitly_wait(5)

    yield driver_instance

    driver_instance.quit()


@pytest.fixture
def admin_credentials():
    return {"username": "admin", "password": "admin"}


@pytest.fixture
def dashboard(driver, base_url, admin_credentials):
    return open_dashboard(
        driver=driver,
        base_url=base_url,
        username=admin_credentials["username"],
        password=admin_credentials["password"],
    )


@pytest.fixture
def users_page(dashboard):
    return UsersPage(dashboard.driver).open()


@pytest.fixture
def statuses_page(dashboard):
    return StatusesPage(dashboard.driver).open()


@pytest.fixture
def labels_page(dashboard):
    return LabelsPage(dashboard.driver).open()


@pytest.fixture
def tasks_page(dashboard):
    return TasksPage(dashboard.driver).open()
