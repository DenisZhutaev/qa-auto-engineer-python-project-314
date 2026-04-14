from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from tests.pages.base_page import BasePage


class StatusFormPage(BasePage):
    FORM = (By.CSS_SELECTOR, "form")
    NAME = (By.CSS_SELECTOR, "form input[name='name']")
    SLUG = (By.CSS_SELECTOR, "form input[name='slug']")
    SAVE_BUTTON = (By.CSS_SELECTOR, "button[aria-label='Save']")
    DELETE_BUTTON = (By.CSS_SELECTOR, "button[aria-label='Delete']")

    def wait_until_loaded(self):
        self.wait_until(EC.visibility_of_element_located(self.FORM))
        self.wait_until(EC.visibility_of_element_located(self.NAME))
        self.wait_until(EC.visibility_of_element_located(self.SLUG))
        return self

    def is_create_form_open(self):
        self.wait_until_loaded()
        return "/create" in self.driver.current_url and not self.driver.find_elements(*self.DELETE_BUTTON)

    def get_values(self):
        self.wait_until_loaded()
        return {
            "name": self.driver.find_element(*self.NAME).get_attribute("value"),
            "slug": self.driver.find_element(*self.SLUG).get_attribute("value"),
        }

    def fill(self, name, slug):
        self._set_input(self.NAME, name)
        self._set_input(self.SLUG, slug)

    def save(self):
        self.wait_until(EC.element_to_be_clickable(self.SAVE_BUTTON)).click()

    def delete(self):
        self.wait_until(EC.element_to_be_clickable(self.DELETE_BUTTON)).click()

    def _set_input(self, locator, value):
        field = self.wait_until(EC.visibility_of_element_located(locator))
        self.driver.execute_script(
            """
            const input = arguments[0];
            const nextValue = arguments[1];
            const nativeSetter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype,
                'value'
            ).set;
            nativeSetter.call(input, nextValue);
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
            """,
            field,
            value,
        )
