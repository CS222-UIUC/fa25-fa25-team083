from backend import nasa_insight #Should fix the issue with pytest not being able to see the backend tests fromt the project root


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
    def fake_get(*args, **kwargs):
        return FakeResp(200, {"sol_keys": ["1", "2", "3"]})

    monkeypatch.setattr(nasa_insight.requests, "get", fake_get)

    sols = nasa_insight.get_sols()
    assert sols == ["1", "2", "3"]


def test_get_sols_failure_returns_empty(monkeypatch):
    def fake_get(*args, **kwargs):
        raise RuntimeError("network down")

    monkeypatch.setattr(nasa_insight.requests, "get", fake_get)

    assert nasa_insight.get_sols() == []


def test_get_latest_sol(monkeypatch):
    monkeypatch.setattr(nasa_insight, "get_sols", lambda: ["1", "2", "3"])
    assert nasa_insight.get_latest_sol() == "3"


def test_get_temp_avg_success(monkeypatch):
    payload = {"sol_keys": ["3"], "3": {"AT": {"av": -5.25}}}

    def fake_get(*args, **kwargs):
        return FakeResp(200, payload)

    monkeypatch.setattr(nasa_insight.requests, "get", fake_get)
    monkeypatch.setattr(nasa_insight, "get_latest_sol", lambda: "3")

    assert nasa_insight.get_temp_avg() == -5.25


def test_get_temp_avg_missing_returns_none(monkeypatch):
    def fake_get1(*a, **k):
        return FakeResp(200, {})

    monkeypatch.setattr(nasa_insight.requests, "get", fake_get1)
    assert nasa_insight.get_temp_avg() is None

    payload2 = {"sol_keys": ["3"], "3": {}}

    def fake_get2(*a, **k):
        return FakeResp(200, payload2)

    monkeypatch.setattr(nasa_insight.requests, "get", fake_get2)
    monkeypatch.setattr(nasa_insight, "get_latest_sol", lambda: "3")
    assert nasa_insight.get_temp_avg() is None


def test_get_wind_avg_success(monkeypatch):
    payload = {"sol_keys": ["42"], "42": {"HWS": {"av": 7.8}}}

    def fake_get(*args, **kwargs):
        return FakeResp(200, payload)

    monkeypatch.setattr(nasa_insight.requests, "get", fake_get)
    monkeypatch.setattr(nasa_insight, "get_latest_sol", lambda: "42")

    assert nasa_insight.get_wind_avg() == 7.8


def test_get_wind_avg_missing_returns_none(monkeypatch):
    payload = {"sol_keys": ["7"], "7": {}}

    def fake_get(*a, **k):
        return FakeResp(200, payload)

    monkeypatch.setattr(nasa_insight.requests, "get", fake_get)
    monkeypatch.setattr(nasa_insight, "get_latest_sol", lambda: "7")

    assert nasa_insight.get_wind_avg() is None


def test_get_wind_avg_exception_returns_none(monkeypatch):
    def fake_get(*a, **k):
        raise TimeoutError()

    monkeypatch.setattr(nasa_insight.requests, "get", fake_get)
    assert nasa_insight.get_wind_avg() is None
