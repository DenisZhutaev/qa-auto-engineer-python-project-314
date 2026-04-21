from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.pages.task_form_page import TaskFormPage


class FakeElement:
    def __init__(self, text="", displayed=True):
        self.text = text
        self._displayed = displayed
        self.clicked = 0
        self.keys = []

    def is_displayed(self):
        return self._displayed

    def click(self):
        self.clicked += 1

    def send_keys(self, value):
        self.keys.append(value)


class FakeDriver:
    def __init__(self):
        self.elements_by_tag = {"body": FakeElement()}
        self.elements_by_xpath = {}
        self.scripts = []

    def find_element(self, by, value):
        if by == By.TAG_NAME:
            return self.elements_by_tag[value]
        raise AssertionError(f"Unexpected find_element call: {by} {value}")

    def find_elements(self, by, value):
        if by == By.XPATH:
            return self.elements_by_xpath.get(value, [])
        raise AssertionError(f"Unexpected find_elements call: {by} {value}")

    def execute_script(self, script, *args):
        self.scripts.append((script, args))
        if "textContent" in script:
            return "  fallback text  "
        return None


def test_xpath_literal_escapes_single_quotes():
    assert TaskFormPage._xpath_literal("alpha") == "'alpha'"
    assert "concat(" in TaskFormPage._xpath_literal("it's ok")


def test_option_text_uses_dom_text_when_visible_text_is_empty():
    driver = FakeDriver()
    page = TaskFormPage(driver)
    option = FakeElement(text="   ")

    assert page._option_text(option).strip() == "fallback text"


def test_visible_options_returns_only_displayed_elements():
    driver = FakeDriver()
    page = TaskFormPage(driver)
    driver.elements_by_xpath[
        "//li[@role='option'] | //*[@role='option' and self::div]"
    ] = [FakeElement(displayed=True), FakeElement(displayed=False)]

    visible = page._visible_options()

    assert len(visible) == 1


def test_open_combobox_retries_after_click_intercept(monkeypatch):
    driver = FakeDriver()
    page = TaskFormPage(driver)
    combobox = FakeElement()

    def flaky_click():
        if combobox.clicked == 0:
            combobox.clicked += 1
            raise ElementClickInterceptedException("intercepted")
        combobox.clicked += 1

    combobox.click = flaky_click
    monkeypatch.setattr(page, "wait_until", lambda *_args, **_kwargs: combobox)

    page._open_combobox((By.XPATH, "//fake"))

    assert combobox.clicked == 2
    assert any("scrollIntoView" in call[0] for call in driver.scripts)


def test_find_option_falls_back_to_displayed_xpath_element(monkeypatch):
    driver = FakeDriver()
    page = TaskFormPage(driver)
    shown = FakeElement("Draft", displayed=True)
    hidden = FakeElement("Draft", displayed=False)
    xpaths = page._option_xpaths(page._xpath_literal("Draft"))
    for xpath in xpaths:
        driver.elements_by_xpath[xpath] = [hidden, shown]

    def raise_timeout(*_args, **_kwargs):
        raise TimeoutException()

    monkeypatch.setattr(page, "wait_until", raise_timeout)

    option = page._find_option("Draft")

    assert option is shown


def test_select_option_uses_keyboard_fallback_when_enabled(monkeypatch):
    driver = FakeDriver()
    page = TaskFormPage(driver)
    combobox = FakeElement()
    body = driver.elements_by_tag["body"]

    monkeypatch.setattr(page, "_open_combobox", lambda _locator: combobox)
    monkeypatch.setattr(page, "_find_option", lambda _text: None)
    monkeypatch.setattr(page, "_visible_options", lambda: [])

    page._select_option("Assignee", "missing", fallback_to_first=True)

    assert combobox.keys == [Keys.ARROW_DOWN, Keys.ENTER]
    assert body.keys.count(Keys.ESCAPE) >= 1
