from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def wait_until(self, condition, timeout=None):
        wait_timeout = timeout if timeout is not None else self.timeout
        return WebDriverWait(self.driver, wait_timeout).until(condition)

    def exists(self, locator, timeout=2):
        from selenium.webdriver.support import expected_conditions as EC

        try:
            self.wait_until(
                EC.visibility_of_element_located(locator),
                timeout=timeout,
            )
            return True
        except TimeoutException:
            return False
