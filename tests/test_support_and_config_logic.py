import pytest
from _pytest.outcomes import Exit

from tests import conftest
from tests.support import session


class DummySession:
    def __init__(self, impl):
        self.config = type("Config", (), {"invocation_params": type(
            "Params", (), {"args": []}
        )()})()
        self.impl = impl


def test_pytest_sessionstart_stops_for_wrong_impl(monkeypatch):
    monkeypatch.setenv("IMPLEMENTATION", "wrong1")
    monkeypatch.delenv("RUN_WRONG_IMPLEMENTATION_TESTS", raising=False)

    with pytest.raises(Exit):
        conftest.pytest_sessionstart(DummySession("wrong1"))


def test_pytest_sessionstart_allows_wrong_impl_when_opted_in(monkeypatch):
    monkeypatch.setenv("IMPLEMENTATION", "wrong2")
    monkeypatch.setenv("RUN_WRONG_IMPLEMENTATION_TESTS", "1")

    # Should not raise when explicitly allowed.
    conftest.pytest_sessionstart(DummySession("wrong2"))


def test_base_url_prefers_app_base_url(monkeypatch):
    monkeypatch.setenv("APP_BASE_URL", "https://example.test")
    base_url_func = conftest.base_url.__wrapped__

    assert base_url_func() == "https://example.test"


def test_base_url_uses_docker_host_when_in_container(monkeypatch):
    monkeypatch.delenv("APP_BASE_URL", raising=False)
    monkeypatch.setenv("APP_BASE_SCHEME", "http")
    monkeypatch.setattr(
        conftest.os.path, "exists", lambda p: p == "/.dockerenv"
    )
    base_url_func = conftest.base_url.__wrapped__

    assert base_url_func() == "http://server"


def test_base_url_uses_localhost_by_default(monkeypatch):
    monkeypatch.delenv("APP_BASE_URL", raising=False)
    monkeypatch.delenv("APP_BASE_SCHEME", raising=False)
    monkeypatch.setattr(conftest.os.path, "exists", lambda _p: False)
    base_url_func = conftest.base_url.__wrapped__

    assert base_url_func() == "http://localhost:5173"


def test_open_dashboard_logs_in_when_login_form_is_visible(monkeypatch):
    calls = []

    class FakeLoginPage:
        def __init__(self, _driver, _base_url):
            pass

        def open(self):
            return self

        def is_displayed(self, timeout):
            return timeout == 3

        def login(self, username, password):
            calls.append(("login", username, password))

    class FakeDashboardPage:
        def __init__(self, _driver):
            pass

        def wait_until_loaded(self):
            calls.append(("loaded",))

    monkeypatch.setattr(session, "LoginPage", FakeLoginPage)
    monkeypatch.setattr(session, "DashboardPage", FakeDashboardPage)

    page = session.open_dashboard("driver", "http://localhost", "u", "p")

    assert calls == [("login", "u", "p"), ("loaded",)]
    assert isinstance(page, FakeDashboardPage)


def test_ensure_login_page_logs_out_when_already_authenticated(monkeypatch):
    calls = []

    class FakeLoginPage:
        def __init__(self, _driver, _base_url):
            self._checks = 0

        def open(self):
            return self

        def is_displayed(self, timeout):
            self._checks += 1
            if timeout == 3:
                return False
            return True

    class FakeDashboardPage:
        def __init__(self, _driver):
            pass

        def logout(self):
            calls.append("logout")

    monkeypatch.setattr(session, "LoginPage", FakeLoginPage)
    monkeypatch.setattr(session, "DashboardPage", FakeDashboardPage)

    login_page, dashboard_page, username, password = session.ensure_login_page(
        "driver", "http://localhost", "admin", "admin"
    )

    assert calls == ["logout"]
    assert username == "admin"
    assert password == "admin"
    assert isinstance(login_page, FakeLoginPage)
    assert isinstance(dashboard_page, FakeDashboardPage)
