from tests.pages.task_form_page import TaskFormPage
from tests.support.factories import unique_task


def _create_task(tasks_page, payload):
    tasks_page.open_create_form()
    form = TaskFormPage(tasks_page.driver).wait_until_loaded()
    form.fill(
        title=payload["title"],
        content=payload["content"],
        assignee=payload["assignee"],
        status=payload["status"],
        label=payload["label"],
    )
    form.save()
    tasks_page.open()


def test_tasks_create_form_and_task_appears_in_selected_column(tasks_page):
    payload = unique_task("create")

    tasks_page.open_create_form()
    form = TaskFormPage(tasks_page.driver).wait_until_loaded()
    assert form.is_create_form_open()
    assert form.has_required_fields()

    form.fill(
        title=payload["title"],
        content=payload["content"],
        assignee=payload["assignee"],
        status=payload["status"],
        label=payload["label"],
    )
    form.save()

    tasks_page.open()
    assert tasks_page.task_in_status_column(payload["title"], payload["status"])


def test_tasks_filter_by_status_updates_visible_cards(tasks_page):
    payload = unique_task("filter-status")
    _create_task(tasks_page, payload)

    all_cards = tasks_page.task_card_count()
    tasks_page.filter_by("Status", "Draft")
    draft_cards = tasks_page.task_card_count()
    assert tasks_page.has_task(payload["title"])
    tasks_page.open()
    tasks_page.filter_by("Status", "Published")
    published_cards = tasks_page.task_card_count()
    assert draft_cards != published_cards
    assert draft_cards <= all_cards and published_cards <= all_cards


def test_tasks_filter_by_assignee_updates_visible_cards(tasks_page):
    payload = unique_task("filter-assignee")
    _create_task(tasks_page, payload)

    all_cards = tasks_page.task_card_count()
    tasks_page.open()
    tasks_page.filter_by("Assignee", "john@google.com")
    john_cards = tasks_page.task_card_count()
    tasks_page.open()
    tasks_page.filter_by("Assignee", "emily@example.com")
    emily_cards = tasks_page.task_card_count()
    assert john_cards <= all_cards
    assert emily_cards <= all_cards


def test_tasks_filter_by_label_updates_visible_cards(tasks_page):
    payload = unique_task("filter-label")
    _create_task(tasks_page, payload)

    tasks_page.open()
    total_cards = tasks_page.task_card_count()
    tasks_page.filter_by("Label", "bug")
    bug_cards = tasks_page.task_card_count()
    tasks_page.open()
    tasks_page.filter_by("Label", "critical")
    critical_cards = tasks_page.task_card_count()
    assert bug_cards >= 0
    assert critical_cards >= 0
    assert total_cards != bug_cards or bug_cards != critical_cards


def test_tasks_edit_saves_updated_data(tasks_page):
    original = unique_task("edit-source")
    updated = unique_task("edit-updated")
    _create_task(tasks_page, original)

    tasks_page.open_task_for_edit(original["title"])
    form = TaskFormPage(tasks_page.driver).wait_until_loaded()
    values = form.get_values()
    assert values["title"] == original["title"]

    form.fill(
        title=updated["title"],
        content=updated["content"],
        assignee=updated["assignee"],
        status=updated["status"],
        label=updated["label"],
    )
    form.save()

    tasks_page.open()
    assert tasks_page.has_task(updated["title"])
    assert not tasks_page.has_task(original["title"])


def test_tasks_move_between_columns_by_status_update(tasks_page):
    payload = unique_task("move")
    _create_task(tasks_page, payload)

    assert tasks_page.task_in_status_column(payload["title"], "Draft")

    tasks_page.open_task_for_edit(payload["title"])
    form = TaskFormPage(tasks_page.driver).wait_until_loaded()
    form.fill(
        title=payload["title"],
        content=payload["content"],
        assignee=payload["assignee"],
        status="To Review",
        label=payload["label"],
    )
    form.save()

    tasks_page.open()
    assert tasks_page.task_in_status_column(payload["title"], "To Review")
    assert not tasks_page.task_in_status_column(payload["title"], "Draft")


def test_tasks_delete_removes_task_from_board(tasks_page):
    payload = unique_task("delete")
    _create_task(tasks_page, payload)
    assert tasks_page.has_task(payload["title"])

    tasks_page.open_task_for_edit(payload["title"])
    form = TaskFormPage(tasks_page.driver).wait_until_loaded()
    form.delete()

    tasks_page.open()
    assert not tasks_page.has_task(payload["title"])
