from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from tests.pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME_LOCATORS = (
        (By.CSS_SELECTOR, "input[name='username']"),
        (By.CSS_SELECTOR, "input[name='email']"),
        (By.CSS_SELECTOR, "input[type='email']"),
        (By.CSS_SELECTOR, "input[type='text']"),
    )
    PASSWORD_LOCATOR = (By.CSS_SELECTOR, "input[type='password']")
    SUBMIT_LOCATOR = (By.CSS_SELECTOR, "button[type='submit']")

    def __init__(self, driver, base_url):
        super().__init__(driver)
        self.base_url = base_url

    def open(self):
        self.driver.get(self.base_url)
        return self

    def is_displayed(self, timeout=5):
        has_password = self.exists(self.PASSWORD_LOCATOR, timeout=timeout)
        has_submit = self.exists(self.SUBMIT_LOCATOR, timeout=timeout)
        has_username = self._find_username_input(timeout=timeout) is not None
        return has_password and has_submit and has_username

    def has_username_input(self, timeout=5):
        return self._find_username_input(timeout=timeout) is not None

    def login(self, username, password):
        username_input = self._find_username_input(timeout=10)
        if username_input is None:
            raise AssertionError("Login input was not found on the page")

        password_input = self.wait_until(
            EC.visibility_of_element_located(self.PASSWORD_LOCATOR)
        )
        submit_button = self.wait_until(
            EC.element_to_be_clickable(self.SUBMIT_LOCATOR)
        )

        username_input.clear()
        username_input.send_keys(username)
        password_input.clear()
        password_input.send_keys(password)
        submit_button.click()

    def _find_username_input(self, timeout=5):
        for locator in self.USERNAME_LOCATORS:
            if self.exists(locator, timeout=timeout):
                return self.driver.find_element(*locator)
        return None
