from tests.support.session import ensure_login_page


def test_user_can_login(driver, base_url, admin_credentials):
    login_page, dashboard_page, username, password = ensure_login_page(
        driver=driver,
        base_url=base_url,
        username=admin_credentials["username"],
        password=admin_credentials["password"],
    )

    login_page.login(username, password)
    dashboard_page.wait_until_loaded()

    assert dashboard_page.has_menu_item("Tasks")
    assert dashboard_page.has_menu_item("Users")


def test_user_can_logout(driver, base_url, admin_credentials):
    login_page, dashboard_page, username, password = ensure_login_page(
        driver=driver,
        base_url=base_url,
        username=admin_credentials["username"],
        password=admin_credentials["password"],
    )

    login_page.login(username, password)
    dashboard_page.wait_until_loaded()
    dashboard_page.logout()

    assert login_page.is_displayed(timeout=10)
