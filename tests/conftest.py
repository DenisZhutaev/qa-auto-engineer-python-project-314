import os

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
    return os.getenv("APP_BASE_URL", "http://localhost:5173")


@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

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
