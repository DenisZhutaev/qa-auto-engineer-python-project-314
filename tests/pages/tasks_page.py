from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from tests.pages.base_page import BasePage


class TasksPage(BasePage):
    MENU_TASKS = (By.XPATH, "//a[contains(normalize-space(), 'Tasks')]")
    PAGE_TITLE = (By.XPATH, "//*[@id='react-admin-title']//*[contains(normalize-space(), 'Tasks')]")
    MAIN_CONTENT = (By.CSS_SELECTOR, "#main-content")
    CREATE_BUTTON = (By.XPATH, "//a[@aria-label='Create' or contains(normalize-space(), 'Create')]")

    def open(self):
        self.wait_until(EC.element_to_be_clickable(self.MENU_TASKS)).click()
        self.wait_until_loaded()
        return self

    def wait_until_loaded(self):
        self.wait_until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait_until(EC.presence_of_element_located(self.MAIN_CONTENT))
        return self

    def open_create_form(self):
        self.wait_until(EC.element_to_be_clickable(self.CREATE_BUTTON)).click()

    def has_task(self, title):
        locator = (
            By.XPATH,
            f"//*[@id='main-content']//*[contains(@class, 'MuiTypography-h5') and normalize-space()='{title}']",
        )
        return any(el.is_displayed() for el in self.driver.find_elements(*locator))

    def task_card_count(self):
        cards = self.driver.find_elements(
            By.XPATH, "//*[@id='main-content']//*[contains(@class, 'MuiTypography-h5')]"
        )
        return sum(1 for c in cards if c.is_displayed())

    def task_in_status_column(self, title, status):
        locator = (
            By.XPATH,
            f"//h6[normalize-space()='{status}']/following-sibling::div[1]//*[contains(@class, 'MuiTypography-h5') and normalize-space()='{title}']",
        )
        return any(el.is_displayed() for el in self.driver.find_elements(*locator))

    def open_task_for_edit(self, title):
        edit_link = (
            By.XPATH,
            f"//*[contains(@class, 'MuiCard-root')][.//*[contains(@class, 'MuiTypography-h5') and normalize-space()='{title}']]//a[@aria-label='Edit']",
        )
        self.wait_until(EC.element_to_be_clickable(edit_link)).click()

    def filter_by(self, label, option_text):
        self._select_option_in_area(
            container_xpath="//*[@id='main-content']",
            label=label,
            option_text=option_text,
        )
        self.wait_until_loaded()

    def _select_option_in_area(self, container_xpath, label, option_text):
        combobox_locator = (
            By.XPATH,
            f"{container_xpath}//label[contains(normalize-space(), '{label}')]/ancestor::*[contains(@class, 'MuiFormControl-root')][1]//*[@role='combobox']",
        )
        combobox = self.wait_until(EC.element_to_be_clickable(combobox_locator))
        try:
            combobox.click()
        except ElementClickInterceptedException:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", combobox
            )
            combobox.click()
        option_xpath = (
            f"//li[normalize-space()='{option_text}' and @role='option'] | "
            f"//*[@role='option' and normalize-space()='{option_text}']"
        )

        def first_visible_matching_option(driver):
            for el in driver.find_elements(By.XPATH, option_xpath):
                if el.is_displayed():
                    return el
            return False

        option = self.wait_until(first_visible_matching_option)
        # Long MUI menus can stack overlapping <li>; native click hits the wrong layer.
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", option)
        self.driver.execute_script("arguments[0].click();", option)
