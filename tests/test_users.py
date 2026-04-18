from tests.pages.user_form_page import UserFormPage
from tests.support.factories import unique_user


def _create_user(users_page, user_data):
    users_page.open_create_form()
    form = UserFormPage(users_page.driver).wait_until_loaded()
    form.fill(user_data["email"], user_data["first_name"], user_data["last_name"])
    form.save()
    users_page.open()


def test_users_create_form_opens_and_new_user_appears_in_list(users_page):
    users_page.clear_all_users()

    new_user = unique_user("create")
    users_page.open_create_form()
    user_form = UserFormPage(users_page.driver).wait_until_loaded()

    assert user_form.is_create_form_open()
    user_form.fill("invalid-email", new_user["first_name"], new_user["last_name"])
    user_form.save()
    assert "email format" in user_form.email_error_text().lower()

    user_form.fill(new_user["email"], new_user["first_name"], new_user["last_name"])
    user_form.save()

    users_page.open()
    assert users_page.has_user(new_user["email"])


def test_users_list_shows_required_columns(users_page):
    headers = users_page.column_headers()

    assert any("Email" in header for header in headers)
    assert any("First name" in header for header in headers)
    assert any("Last name" in header for header in headers)


def test_users_edit_prefills_data_and_updates_values(users_page):
    users_page.clear_all_users()

    original_user = unique_user("source")
    updated_user = unique_user("updated")
    _create_user(users_page, original_user)

    users_page.open_user(original_user["email"])
    form = UserFormPage(users_page.driver).wait_until_loaded()
    values = form.get_values()
    assert values["email"] == original_user["email"]
    assert values["first_name"] == original_user["first_name"]
    assert values["last_name"] == original_user["last_name"]

    form.fill(updated_user["email"], updated_user["first_name"], updated_user["last_name"])
    form.save()
    users_page.open()

    assert users_page.has_user(updated_user["email"])
    assert not users_page.has_user(original_user["email"])


def test_users_delete_removes_user_from_list(users_page):
    users_page.clear_all_users()

    removable_user = unique_user("remove")
    keep_user = unique_user("keep")
    _create_user(users_page, removable_user)
    _create_user(users_page, keep_user)

    users_page.open_user(removable_user["email"])
    form = UserFormPage(users_page.driver).wait_until_loaded()
    form.delete()
    users_page.confirm_delete_if_dialog_present()
    users_page.wait_until_loaded()

    assert not users_page.has_user(removable_user["email"])
    assert users_page.has_user(keep_user["email"])


def test_users_bulk_delete_clears_all_selected_users(users_page):
    users_page.clear_all_users()

    _create_user(users_page, unique_user("bulkone"))
    _create_user(users_page, unique_user("bulktwo"))
    assert users_page.row_count() == 2

    users_page.bulk_delete_all()
    assert users_page.row_count() == 0
