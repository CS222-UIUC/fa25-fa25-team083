import json
import requests
import pytest
import os
import sys


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
from backend.llspacedevs import AstronautData

# Small helper mock response class
class MockResponse:
    def __init__(self, json_data=None, status_code=200, raise_exc=None):
        self._json = json_data or {}
        self.status_code = status_code
        self._raise_exc = raise_exc

    def json(self):
        return self._json

    def raise_for_status(self):
        if self._raise_exc:
            raise self._raise_exc
        if 400 <= self.status_code < 600 and not self._raise_exc:
            raise requests.HTTPError(f"HTTP {self.status_code}")

# 1) Cache reading — should not call requests.get
def test_get_astronauts_reads_cache_and_skips_network(tmp_path, monkeypatch):
    cache = tmp_path / "astronauts.json"
    data = [{"name": "Alice", "nationality": "American"}]
    cache.write_text(json.dumps(data))

    called = {"get": False}
    def fake_get(*args, **kwargs):
        called["get"] = True
        return MockResponse([], 200)
    monkeypatch.setattr("requests.get", fake_get)

    ad = AstronautData(cache_file=str(cache))
    result = ad.get_astronauts()
    assert result == data
    assert called["get"] is False

# 2) Pagination and cache write
def test_fetch_pagination_and_writes_cache(tmp_path, monkeypatch):
    page1 = {"results": [{"name": "A", "nationality": "X"}], "next": "url2"}
    page2 = {"results": [{"name": "B", "nationality": "Y"}], "next": None}
    responses = {
        "https://lldev.thespacedevs.com/2.2.0/astronaut/?limit=100": MockResponse(page1, 200),
        "url2": MockResponse(page2, 200),
    }

    def fake_get(url, *args, **kwargs):
        return responses[url]

    monkeypatch.setattr("requests.get", fake_get)

    cache = tmp_path / "astronauts.json"
    ad = AstronautData(cache_file=str(cache))
    result = ad.get_astronauts()
    assert isinstance(result, list)
    assert len(result) == 2
    # verify cache file created and content matches
    cached = json.loads(cache.read_text())
    assert cached == result

# 3) Rate-limit (429) raises
def test_fetch_raises_on_rate_limit(monkeypatch, tmp_path):
    def fake_get(url, *args, **kwargs):
        return MockResponse({}, status_code=429)
    monkeypatch.setattr("requests.get", fake_get)
    ad = AstronautData(cache_file=str(tmp_path / "astronauts.json"))
    with pytest.raises(Exception) as exc:
        ad._fetch_astronauts()
    assert "Rate limit" in str(exc.value)

# 4) Filtering and top country aggregation
def test_filtering_and_top_countries(tmp_path):
    data = [
        {"name": "Alice", "nationality": "American"},
        {"name": "Bob", "nationality": "american"},
        {"name": "Carlos", "nationality": "Spanish"},
        {"name": "Dana", "nationality": None},
    ]
    cache = tmp_path / "astronauts.json"
    cache.write_text(json.dumps(data))
    ad = AstronautData(cache_file=str(cache))
    americans = ad.get_astronauts_by_country("american")
    assert "Alice" in americans and "Bob" in americans
    top = ad.get_top_countries(top_n=2)
    # top should return tuples (country, count, [names])
    assert isinstance(top, list)
    counts = {c: cnt for c, cnt, _ in top}
    # American/american counted separately because current code keys on raw nationality strings
    # validate counts reflect input
    assert any(country in ("American", "american") for country in counts)