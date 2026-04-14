from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from tests.pages.base_page import BasePage


class TaskFormPage(BasePage):
    FORM = (By.CSS_SELECTOR, "form")
    TITLE = (By.CSS_SELECTOR, "form input[name='title']")
    CONTENT = (By.CSS_SELECTOR, "form textarea[name='content']")
    SAVE_BUTTON = (By.CSS_SELECTOR, "button[aria-label='Save']")
    DELETE_BUTTON = (By.CSS_SELECTOR, "button[aria-label='Delete']")

    def wait_until_loaded(self):
        self.wait_until(EC.visibility_of_element_located(self.FORM))
        self.wait_until(EC.visibility_of_element_located(self.TITLE))
        return self

    def is_create_form_open(self):
        self.wait_until_loaded()
        return "/create" in self.driver.current_url

    def has_required_fields(self):
        form_text = self.driver.find_element(*self.FORM).text
        return "Title" in form_text and "Assignee" in form_text and "Status" in form_text

    def fill(self, title, content, assignee, status, label):
        self._set_input(self.TITLE, title)
        self._set_input(self.CONTENT, content)
        self._select_option("Assignee", assignee)
        self._select_option("Status", status)
        if label:
            self._select_option("Label", label)

    def get_values(self):
        return {
            "title": self.driver.find_element(*self.TITLE).get_attribute("value"),
            "content": self.driver.find_element(*self.CONTENT).get_attribute("value"),
        }

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
                Object.getPrototypeOf(input),
                'value'
            ).set;
            nativeSetter.call(input, nextValue);
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
            """,
            field,
            value,
        )

    def _select_option(self, label, option_text):
        combobox_locator = (
            By.XPATH,
            f"//form//label[contains(normalize-space(), '{label}')]/ancestor::*[contains(@class, 'MuiFormControl-root')][1]//*[@role='combobox']",
        )
        self.wait_until(EC.element_to_be_clickable(combobox_locator)).click()
        option_locator = (
            By.XPATH,
            f"//li[normalize-space()='{option_text}' and @role='option'] | //*[@role='option' and normalize-space()='{option_text}']",
        )
        self.wait_until(EC.element_to_be_clickable(option_locator)).click()
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
