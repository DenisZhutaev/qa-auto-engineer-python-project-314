from tests.pages.label_form_page import LabelFormPage
from tests.support.factories import unique_label


def _create_label(labels_page, name):
    labels_page.open_create_form()
    form = LabelFormPage(labels_page.driver).wait_until_loaded()
    form.fill_name(name)
    form.save()
    labels_page.open()


def test_labels_create_form_opens_and_new_label_appears_in_list(labels_page):
    labels_page.clear_all_labels()

    new_label = unique_label("created")
    labels_page.open_create_form()
    form = LabelFormPage(labels_page.driver).wait_until_loaded()

    assert form.is_create_form_open()
    form.fill_name(new_label)
    form.save()
    labels_page.open()

    assert labels_page.has_label(new_label)


def test_labels_list_loads_and_shows_records(labels_page):
    headers = labels_page.column_headers()

    assert any("Name" in header for header in headers)
    assert labels_page.row_count() >= 1


def test_labels_edit_updates_saved_values(labels_page):
    labels_page.clear_all_labels()

    original_name = unique_label("source")
    updated_name = unique_label("updated")
    _create_label(labels_page, original_name)

    labels_page.open_label(original_name)
    form = LabelFormPage(labels_page.driver).wait_until_loaded()
    assert form.get_name() == original_name

    form.fill_name(updated_name)
    form.save()
    labels_page.open()

    assert labels_page.has_label(updated_name)
    assert not labels_page.has_label(original_name)


def test_labels_delete_one_or_multiple_from_list(labels_page):
    labels_page.clear_all_labels()

    first_label = unique_label("remove")
    second_label = unique_label("remove")
    _create_label(labels_page, first_label)
    _create_label(labels_page, second_label)

    labels_page.open_label(first_label)
    form = LabelFormPage(labels_page.driver).wait_until_loaded()
    form.delete()
    labels_page.confirm_delete_if_dialog_present()
    labels_page.open()
    assert not labels_page.has_label(first_label)

    labels_page.open_label(second_label)
    form = LabelFormPage(labels_page.driver).wait_until_loaded()
    form.delete()
    labels_page.confirm_delete_if_dialog_present()
    labels_page.open()
    assert not labels_page.has_label(second_label)
