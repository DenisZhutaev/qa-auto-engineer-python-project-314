from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from tests.pages.base_page import BasePage


class ResourceListPage(BasePage):
    TABLE = (By.CSS_SELECTOR, "table")
    ROWS = (By.CSS_SELECTOR, "tbody tr")
    CREATE_BUTTON = (
        By.XPATH,
        "//a[@aria-label='Create' or contains(normalize-space(), 'Create')]",
    )
    SELECT_ALL = (By.CSS_SELECTOR, "input[aria-label='Select all']")
    BULK_TOOLBAR = (By.CSS_SELECTOR, "[data-test='bulk-actions-toolbar']")
    BULK_DELETE = (
        By.CSS_SELECTOR,
        "[data-test='bulk-actions-toolbar'] button[aria-label='Delete']",
    )
    HEADER_CELLS = (By.CSS_SELECTOR, "thead th")

    def __init__(
        self,
        driver,
        menu_text,
        title_text,
        identity_column,
        wait_for_table=True,
    ):
        super().__init__(driver)
        self.menu_text = menu_text
        self.title_text = title_text
        self.identity_column = identity_column
        self.wait_for_table = wait_for_table

    @property
    def menu_locator(self):
        return (
            By.XPATH,
            f"//a[contains(normalize-space(), '{self.menu_text}')]",
        )

    @property
    def title_locator(self):
        return (
            By.XPATH,
            "//*[@id='react-admin-title']//*[contains("
            f"normalize-space(), '{self.title_text}')]",
        )

    def open(self):
        self.wait_until(EC.element_to_be_clickable(self.menu_locator)).click()
        self.wait_until_loaded()
        return self

    def wait_until_loaded(self):
        self.wait_until(EC.visibility_of_element_located(self.title_locator))
        if self.wait_for_table:
            self.wait_until(EC.presence_of_element_located(self.TABLE))
        return self

    def row_count(self):
        return len(self.driver.find_elements(*self.ROWS))

    def column_headers(self):
        return [
            h.text.strip()
            for h in self.driver.find_elements(*self.HEADER_CELLS)
            if h.text.strip()
        ]

    def open_create_form(self):
        self.wait_until(EC.element_to_be_clickable(self.CREATE_BUTTON)).click()

    def has_row(self, value):
        return self._find_row_by_value(value) is not None

    def open_row(self, value):
        row = self._find_row_by_value(value)
        if row is None:
            raise AssertionError(f"Row with value '{value}' was not found")
        row.click()

    def clear_all_rows(self):
        self.wait_until_loaded()
        if self.row_count() == 0:
            return
        self._click_select_all()
        self.wait_until(
            lambda drv: (
                "items selected"
                in drv.find_element(*self.BULK_TOOLBAR).text.lower()
            )
        )
        self._click_visible_bulk_delete()
        self.confirm_delete_if_dialog_present()
        self.wait_until(lambda drv: len(drv.find_elements(*self.ROWS)) == 0)

    def bulk_delete_all(self):
        self.clear_all_rows()

    def confirm_delete_if_dialog_present(self):
        dialogs = self.driver.find_elements(By.CSS_SELECTOR, "[role='dialog']")
        if dialogs:
            delete_buttons = dialogs[0].find_elements(
                By.CSS_SELECTOR,
                "button[aria-label='Delete']",
            )
            if delete_buttons:
                delete_buttons[0].click()

    def _find_row_by_value(self, value):
        locator = (
            By.XPATH,
            "//tbody/tr[.//td[contains(@class, "
            f"'column-{self.identity_column}')]//*[normalize-space()='{value}']]",
        )
        rows = self.driver.find_elements(*locator)
        return rows[0] if rows else None

    def _click_select_all(self):
        checkbox = self.wait_until(
            EC.presence_of_element_located(self.SELECT_ALL)
        )
        self.driver.execute_script("arguments[0].click();", checkbox)

    def _click_visible_bulk_delete(self):
        delete_buttons = self.driver.find_elements(*self.BULK_DELETE)
        for button in delete_buttons:
            if button.is_displayed():
                button.click()
                return
        raise AssertionError("Bulk delete button is not visible")
