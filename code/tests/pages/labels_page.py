from tests.pages.resource_list_page import ResourceListPage


class LabelsPage(ResourceListPage):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            menu_text="Labels",
            title_text="Labels",
            identity_column="name",
            wait_for_table=False,
        )

    def has_label(self, name):
        return self.has_row(name)

    def open_label(self, name):
        self.open_row(name)

    def clear_all_labels(self):
        self.clear_all_rows()
