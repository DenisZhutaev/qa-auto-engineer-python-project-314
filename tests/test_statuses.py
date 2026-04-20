from tests.pages.status_form_page import StatusFormPage
from tests.support.factories import unique_status


def _create_status(statuses_page, status_data):
    statuses_page.open_create_form()
    form = StatusFormPage(statuses_page.driver).wait_until_loaded()
    form.fill(status_data["name"], status_data["slug"])
    form.save()
    statuses_page.open()


def test_statuses_create_form_opens_and_new_status_appears_in_list(
    statuses_page,
):
    statuses_page.clear_all_statuses()

    new_status = unique_status("created")
    statuses_page.open_create_form()
    status_form = StatusFormPage(statuses_page.driver).wait_until_loaded()

    assert status_form.is_create_form_open()
    status_form.fill(new_status["name"], new_status["slug"])
    status_form.save()

    statuses_page.open()
    assert statuses_page.has_status(new_status["slug"])


def test_statuses_list_shows_required_columns(statuses_page):
    headers = statuses_page.column_headers()

    assert any("Name" in header for header in headers)
    assert any("Slug" in header for header in headers)
    assert statuses_page.row_count() >= 1


def test_statuses_edit_updates_values(statuses_page):
    statuses_page.clear_all_statuses()

    original_status = unique_status("source")
    updated_status = unique_status("updated")
    _create_status(statuses_page, original_status)

    statuses_page.open_status(original_status["slug"])
    form = StatusFormPage(statuses_page.driver).wait_until_loaded()
    values = form.get_values()
    assert values["name"] == original_status["name"]
    assert values["slug"] == original_status["slug"]

    form.fill(updated_status["name"], updated_status["slug"])
    form.save()
    statuses_page.open()

    assert statuses_page.has_status(updated_status["slug"])
    assert not statuses_page.has_status(original_status["slug"])


def test_statuses_delete_removes_status_from_list(statuses_page):
    statuses_page.clear_all_statuses()

    removable_status = unique_status("remove")
    keep_status = unique_status("keep")
    _create_status(statuses_page, removable_status)
    _create_status(statuses_page, keep_status)

    statuses_page.open_status(removable_status["slug"])
    form = StatusFormPage(statuses_page.driver).wait_until_loaded()
    form.delete()
    statuses_page.confirm_delete_if_dialog_present()
    statuses_page.wait_until_loaded()

    assert not statuses_page.has_status(removable_status["slug"])
    assert statuses_page.has_status(keep_status["slug"])


def test_statuses_bulk_delete_clears_all_selected_statuses(statuses_page):
    statuses_page.clear_all_statuses()

    _create_status(statuses_page, unique_status("bulkone"))
    _create_status(statuses_page, unique_status("bulktwo"))
    assert statuses_page.row_count() == 2

    statuses_page.bulk_delete_all()
    assert statuses_page.row_count() == 0
