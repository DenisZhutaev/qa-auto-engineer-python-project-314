from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
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
        self._select_option("Assignee", assignee, fallback_to_first=True)
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

    @staticmethod
    def _xpath_literal(value):
        """Escape a string for use inside XPath single-quoted literals."""
        if "'" not in value:
            return f"'{value}'"
        parts = value.split("'")
        return "concat(" + ", ".join(
            f"'{p}', \"'\"" if i < len(parts) - 1 else f"'{p}'"
            for i, p in enumerate(parts)
        ) + ")"

    def _option_text(self, element):
        """Visible text; prefer DOM text when Selenium's .text is empty (MUI listbox)."""
        raw = element.text.strip()
        if raw:
            return raw
        return (
            self.driver.execute_script(
                "return (arguments[0].textContent || '').trim();",
                element,
            )
            or ""
        )

    def _visible_options(self):
        """Only options in the open menu; hidden copies often have empty .text in Selenium."""
        return [
            el
            for el in self.driver.find_elements(
                By.XPATH, "//li[@role='option'] | //*[@role='option' and self::div]"
            )
            if el.is_displayed()
        ]

    def _select_option(self, label, option_text, fallback_to_first=False):
        combobox_locator = (
            By.XPATH,
            f"//form//label[contains(normalize-space(), '{label}')]/ancestor::*[contains(@class, 'MuiFormControl-root')][1]//*[@role='combobox']",
        )

        for _ in range(3):
            try:
                combobox = self.wait_until(EC.element_to_be_clickable(combobox_locator))
                # MUI <Select> does not open its listbox on synthetic JS clicks; use a real click.
                try:
                    combobox.click()
                except ElementClickInterceptedException:
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block: 'center'});", combobox
                    )
                    combobox.click()
                option = None

                if option_text:
                    normalized_target = option_text.strip().lower()
                    lit = self._xpath_literal(option_text.strip())
                    # Poll until this option is clickable (same idea as TasksPage.filter_by).
                    option_locator = (
                        By.XPATH,
                        f"//li[@role='option' and normalize-space()={lit}] | "
                        f"//*[@role='option' and normalize-space()={lit}] | "
                        f"//li[@role='option' and contains(normalize-space(), {lit})] | "
                        f"//*[@role='option' and contains(normalize-space(), {lit})]",
                    )
                    try:
                        option = self.wait_until(
                            EC.element_to_be_clickable(option_locator),
                            timeout=self.timeout,
                        )
                    except TimeoutException:
                        for xpath in (
                            f"//li[@role='option' and normalize-space()={lit}]",
                            f"//*[@role='option' and normalize-space()={lit}]",
                            f"//li[@role='option' and contains(normalize-space(), {lit})]",
                            f"//*[@role='option' and contains(normalize-space(), {lit})]",
                        ):
                            for el in self.driver.find_elements(By.XPATH, xpath):
                                if el.is_displayed():
                                    option = el
                                    break
                            if option is not None:
                                break

                    if option is None:
                        for item in self._visible_options():
                            item_text = self._option_text(item).strip().lower()
                            if item_text == normalized_target or normalized_target in item_text:
                                option = item
                                break

                options = self._visible_options()
                if option is None and fallback_to_first and options:
                    option = options[0]

                if option is None:
                    raise TimeoutException(f"Option '{option_text}' was not found for '{label}'")

                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", option)
                self.driver.execute_script("arguments[0].click();", option)
                self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                return
            except (ElementClickInterceptedException, TimeoutException):
                self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                if fallback_to_first:
                    # Keyboard fallback is often more stable in headless CI.
                    try:
                        combobox = self.wait_until(EC.element_to_be_clickable(combobox_locator))
                        try:
                            combobox.click()
                        except ElementClickInterceptedException:
                            self.driver.execute_script(
                                "arguments[0].scrollIntoView({block: 'center'});", combobox
                            )
                            combobox.click()
                        combobox.send_keys(Keys.ARROW_DOWN)
                        combobox.send_keys(Keys.ENTER)
                        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                        return
                    except Exception:
                        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)

        raise AssertionError(f"Could not select '{option_text}' for '{label}'")
