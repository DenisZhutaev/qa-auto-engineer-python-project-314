from tests.pages.dashboard_page import DashboardPage
from tests.pages.login_page import LoginPage


def ensure_login_page(driver, base_url, username="admin", password="admin"):
    login_page = LoginPage(driver, base_url).open()
    dashboard_page = DashboardPage(driver)
    if not login_page.is_displayed(timeout=3):
        dashboard_page.logout()
        assert login_page.is_displayed(timeout=10), (
            "Expected login form after logout"
        )
    return login_page, dashboard_page, username, password


def open_dashboard(driver, base_url, username="admin", password="admin"):
    login_page = LoginPage(driver, base_url).open()
    dashboard_page = DashboardPage(driver)
    if login_page.is_displayed(timeout=3):
        login_page.login(username, password)
    dashboard_page.wait_until_loaded()
    return dashboard_page
