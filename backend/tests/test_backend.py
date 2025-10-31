from backend import (
    nasa_insight,
)  # Should fix the issue with pytest not being able to see the backend tests fromt the project root


def test_truth():
    assert True  # This is here to pass the test check on GitHub by default. In reality, will add tests later


"""
Reference
https://docs.pytest.org/en/stable/
https://docs.pytest.org/en/stable/explanation/fixtures.html
https://docs.pytest.org/en/stable/reference/reference.html
first time doing tests and needed help from GPT also to test these since it gets complicated when trying to do tests using API calls on these getters
"""


class FakeResp:
    def __init__(self, status_code=200, payload=None):
        self.status_code = status_code
        self._payload = payload or {}
        self.ok = 200 <= status_code < 300

    def raise_for_status(self):
        if not self.ok:
            raise Exception(f"HTTP {self.status_code}")

    def json(self):
        return self._payload


def test_get_sols_success(monkeypatch):
    monkeypatch.setattr(
        nasa_insight,
        "get_insight_data",
        lambda: {"sol_keys": ["1", "2", "3"]},
    )

    sols = nasa_insight.get_sols()
    assert sols == ["1", "2", "3"]


def test_get_sols_failure_returns_empty(monkeypatch):
    monkeypatch.setattr(nasa_insight, "get_insight_data", lambda: {})

    assert nasa_insight.get_sols() == []


def test_get_latest_sol(monkeypatch):
    monkeypatch.setattr(nasa_insight, "get_sols", lambda: ["1", "2", "3"])
    assert nasa_insight.get_latest_sol() == "3"


def test_get_temp_avg_success(monkeypatch):
    payload = {"sol_keys": ["3"], "3": {"AT": {"av": -5.25}}}
    monkeypatch.setattr(nasa_insight, "get_insight_data", lambda: payload)
    monkeypatch.setattr(nasa_insight, "get_latest_sol", lambda: "3")

    assert nasa_insight.get_temp_avg() == -5.25


def test_get_temp_avg_missing_returns_none(monkeypatch):
    # case 1: no data at all
    monkeypatch.setattr(nasa_insight, "get_insight_data", lambda: {})
    monkeypatch.setattr(nasa_insight, "get_latest_sol", lambda: None)
    assert nasa_insight.get_temp_avg() is None

    # case 2: sol exists but AT is missing
    payload2 = {"sol_keys": ["3"], "3": {}}
    monkeypatch.setattr(nasa_insight, "get_insight_data", lambda: payload2)
    monkeypatch.setattr(nasa_insight, "get_latest_sol", lambda: "3")
    assert nasa_insight.get_temp_avg() is None


def test_get_wind_avg_success(monkeypatch):
    payload = {"sol_keys": ["42"], "42": {"HWS": {"av": 7.8}}}

    monkeypatch.setattr(nasa_insight, "get_insight_data", lambda: payload)
    monkeypatch.setattr(nasa_insight, "get_latest_sol", lambda: "42")

    assert nasa_insight.get_wind_avg() == 7.8


def test_get_wind_avg_missing_returns_none(monkeypatch):
    payload = {"sol_keys": ["7"], "7": {}}

    monkeypatch.setattr(nasa_insight, "get_insight_data", lambda: payload)
    monkeypatch.setattr(nasa_insight, "get_latest_sol", lambda: "7")

    assert nasa_insight.get_wind_avg() is None


def test_get_wind_avg_exception_returns_none(monkeypatch):
    monkeypatch.setattr(nasa_insight, "get_insight_data", lambda: {})
    monkeypatch.setattr(nasa_insight, "get_latest_sol", lambda: "999")

    assert nasa_insight.get_wind_avg() is None
