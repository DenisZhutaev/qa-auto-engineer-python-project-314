from tests.pages.resource_list_page import ResourceListPage


class UsersPage(ResourceListPage):
    def __init__(self, driver):
        super().__init__(
            driver=driver,
            menu_text="Users",
            title_text="Users",
            identity_column="email",
            wait_for_table=True,
        )

    def has_user(self, email):
        return self.has_row(email)

    def open_user(self, email):
        self.open_row(email)

    def clear_all_users(self):
        self.clear_all_rows()
