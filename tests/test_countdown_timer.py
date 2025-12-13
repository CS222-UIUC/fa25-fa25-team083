import datetime
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# from unittest.mock import MagicMock
import pytest
from backend import (
    nasa_timer,
)

FIXED_NOW = datetime.datetime(2024, 1, 1, 12, 0, 0)


@pytest.fixture
def mock_datetime_now(monkeypatch):
    """Fixture to mock datetime.datetime.now() to return a fixed time."""

    class MockDatetime(datetime.datetime):
        # Override the classmethod 'now'
        @classmethod
        def now(cls, tz=None):

            return (
                FIXED_NOW.replace(tzinfo=tz)
                if tz
                else FIXED_NOW.replace(tzinfo=datetime.timezone.utc)
            )

    monkeypatch.setattr("backend.nasa_timer.datetime.datetime", MockDatetime)


# --- Test Cases ---


def test_countdown_future(mock_datetime_now):
    """Tests a target date in the future."""
    future_target = "2024-01-04T13:30:00"

    result = nasa_timer.get_countdown("Future Launch", future_target)

    assert result.target_name == "Future Launch"
    assert result.days == 3
    assert result.hours == 1
    assert result.minutes == 30
    assert result.seconds == 0


def test_countdown_past(mock_datetime_now):
    """Tests a target date in the past."""
    past_target = "2023-12-25T00:00:00"

    result = nasa_timer.get_countdown("Past Event", past_target)

    assert result.days == 0
    assert result.hours == 0
    assert result.minutes == 0
    assert result.seconds == 0


def test_countdown_near_future(mock_datetime_now):
    """Tests a countdown just a few minutes away."""
    near_future_target = "2024-01-01T12:02:05"

    result = nasa_timer.get_countdown("Quick Test", near_future_target)

    assert result.days == 0
    assert result.hours == 0
    assert result.minutes == 2
    assert result.seconds == 5


def test_countdown_invalid_date():
    """Tests handling of an incorrectly formatted date string."""
    invalid_date = "2024/01/01 12:00"

    result = nasa_timer.get_countdown("Bad Date", invalid_date)

    assert result.days == 0
    assert result.hours == 0
    assert result.minutes == 0
    assert result.seconds == 0
