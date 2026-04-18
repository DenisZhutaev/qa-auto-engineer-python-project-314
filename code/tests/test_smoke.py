from tests.pages.dashboard_page import DashboardPage
from tests.pages.login_page import LoginPage


def test_smoke_app_renders_main_elements(driver, base_url):
    login_page = LoginPage(driver, base_url).open()
    dashboard_page = DashboardPage(driver)

    if login_page.is_displayed(timeout=3):
        assert login_page.has_username_input(timeout=5)
        assert driver.find_element(*login_page.PASSWORD_LOCATOR).is_displayed()
        assert driver.find_element(*login_page.SUBMIT_LOCATOR).is_displayed()
        return

    dashboard_page.wait_until_loaded()
    assert dashboard_page.has_menu_item("Tasks")
    assert dashboard_page.has_menu_item("Users")
