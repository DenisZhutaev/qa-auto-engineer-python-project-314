from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from tests.pages.base_page import BasePage


class DashboardPage(BasePage):
    TITLE_LOCATOR = (
        By.XPATH,
        "//*[contains(normalize-space(), 'Welcome to the administration')]",
    )
    PROFILE_BUTTON = (By.CSS_SELECTOR, "button[aria-label='Profile']")
    LOGOUT_ITEM = (
        By.XPATH,
        "//*[self::a or self::li or self::button]["
        "contains(normalize-space(), 'Logout') or "
        "contains(normalize-space(), 'Sign out') or "
        "contains(normalize-space(), 'Log out')]",
    )

    def wait_until_loaded(self):
        return self.wait_until(
            EC.visibility_of_element_located(self.TITLE_LOCATOR)
        )

    def has_menu_item(self, text):
        locator = (By.XPATH, f"//a[contains(normalize-space(), '{text}')]")
        return self.exists(locator, timeout=5)

    def logout(self):
        profile_button = self.wait_until(
            EC.element_to_be_clickable(self.PROFILE_BUTTON)
        )
        profile_button.click()
        logout_button = self.wait_until(
            EC.element_to_be_clickable(self.LOGOUT_ITEM)
        )
        logout_button.click()
