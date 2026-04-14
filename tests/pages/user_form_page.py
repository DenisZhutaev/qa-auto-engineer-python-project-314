from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from tests.pages.base_page import BasePage


class UserFormPage(BasePage):
    FORM = (By.CSS_SELECTOR, "form")
    EMAIL = (By.CSS_SELECTOR, "form input[name='email']")
    FIRST_NAME = (By.CSS_SELECTOR, "form input[name='firstName']")
    LAST_NAME = (By.CSS_SELECTOR, "form input[name='lastName']")
    SAVE_BUTTON = (By.CSS_SELECTOR, "button[aria-label='Save']")
    DELETE_BUTTON = (By.CSS_SELECTOR, "button[aria-label='Delete']")

    def wait_until_loaded(self):
        self.wait_until(EC.visibility_of_element_located(self.FORM))
        self.wait_until(EC.visibility_of_element_located(self.EMAIL))
        return self

    def is_create_form_open(self):
        self.wait_until_loaded()
        return "/create" in self.driver.current_url and not self.driver.find_elements(*self.DELETE_BUTTON)

    def get_values(self):
        self.wait_until_loaded()
        return {
            "email": self.driver.find_element(*self.EMAIL).get_attribute("value"),
            "first_name": self.driver.find_element(*self.FIRST_NAME).get_attribute("value"),
            "last_name": self.driver.find_element(*self.LAST_NAME).get_attribute("value"),
        }

    def fill(self, email, first_name, last_name):
        self._set_input(self.EMAIL, email)
        self._set_input(self.FIRST_NAME, first_name)
        self._set_input(self.LAST_NAME, last_name)

    def set_email(self, email):
        self._set_input(self.EMAIL, email)

    def email_is_valid(self):
        email_input = self.driver.find_element(*self.EMAIL)
        return self.driver.execute_script("return arguments[0].checkValidity();", email_input)

    def email_validation_message(self):
        return self.driver.find_element(*self.EMAIL).get_attribute("validationMessage")

    def email_error_text(self):
        helpers = self.driver.find_elements(By.CSS_SELECTOR, "p.MuiFormHelperText-root")
        for helper in helpers:
            text = helper.text.strip()
            if text:
                return text
        return ""

    def save(self):
        self.wait_until(EC.element_to_be_clickable(self.SAVE_BUTTON)).click()

    def is_save_enabled(self):
        save_button = self.driver.find_element(*self.SAVE_BUTTON)
        disabled = save_button.get_attribute("disabled")
        return disabled is None

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
