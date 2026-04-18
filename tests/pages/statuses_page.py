from tests.pages.resource_list_page import ResourceListPage


class StatusesPage(ResourceListPage):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            menu_text="Task statuses",
            title_text="Task statuses",
            identity_column="slug",
            wait_for_table=True,
        )

    def has_status(self, slug):
        return self.has_row(slug)

    def open_status(self, slug):
        self.open_row(slug)

    def clear_all_statuses(self):
        self.clear_all_rows()
