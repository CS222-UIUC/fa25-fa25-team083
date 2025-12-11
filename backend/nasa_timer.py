import datetime
from dataclasses import dataclass
import requests
import threading
import time


@dataclass
class CountdownResult:
    """Stores the calculated time remaining."""

    target_name: str
    target_date: str
    days: int
    hours: int
    minutes: int
    seconds: int


def get_countdown(target_name: str, target_datetime_str: str) -> CountdownResult:
    """
    Calculates the time difference between the current time and a target time.
    """
    try:
        # convert the target string to a datetime object
        current_time = datetime.datetime.now(datetime.timezone.utc)

        target_time = datetime.datetime.fromisoformat(target_datetime_str)

        if (
            target_time.tzinfo is None
            or target_time.tzinfo.utcoffset(target_time) is None
        ):
            target_time = target_time.replace(tzinfo=datetime.timezone.utc)

        time_difference = target_time - current_time
        total_seconds = int(time_difference.total_seconds())

        if total_seconds < 0:
            return CountdownResult(target_name, target_datetime_str, 0, 0, 0, 0)

        days = total_seconds // (24 * 3600)
        seconds_remaining = total_seconds % (24 * 3600)
        hours = seconds_remaining // 3600
        minutes = (seconds_remaining % 3600) // 60
        seconds = seconds_remaining % 60

        return CountdownResult(
            target_name=target_name,
            target_date=target_datetime_str,
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
        )
    except Exception:
        return CountdownResult(target_name, target_datetime_str, 0, 0, 0, 0)


def fetch_next_launch() -> tuple[str, str] | None:
    """
    Query a public launches API and return the next upcoming launch's name and
    ISO datetime string (UTC). Returns None on failure.

    Uses TheSpaceDevs Launch Library endpoint (no API key required for basic use).
    """
    # Simple module-level TTL cache for 1 hour to avoid frequent external calls
    # Cache structure: (_cache_value, _cache_timestamp)
    global _launch_cache_value, _launch_cache_time

    # initialize cache variables if not present
    try:
        _launch_cache_value
    except NameError:
        _launch_cache_value = None
        _launch_cache_time = 0

    # TTL in seconds (1 hour)
    TTL = 60 * 60

    # lock for thread-safety
    try:
        _launch_cache_lock
    except NameError:
        _launch_cache_lock = threading.Lock()

    # return cached value if still valid
    with _launch_cache_lock:
        if _launch_cache_value is not None and (time.time() - _launch_cache_time) < TTL:
            return _launch_cache_value

    # otherwise fetch fresh value
    try:
        resp = requests.get(
            "https://ll.thespacedevs.com/2.2.0/launch/upcoming/?limit=1",
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results") or []
        if not results:
            return None
        item = results[0]
        name = item.get("name") or item.get("mission", {}).get("name") or "Upcoming Launch"
        net = item.get("net")
        if not net:
            return None
        value = (name, net)

        # store in cache
        with _launch_cache_lock:
            _launch_cache_value = value
            _launch_cache_time = time.time()

        return value
    except Exception:
        return None


# example
if __name__ == "__main__":
    target = "2025-09-01T10:00:00"
    countdown = get_countdown("Artemis II Launch", target)
    print(f"Countdown for {countdown.target_name}:")
    print(
        f"{countdown.days} days, {countdown.hours} hours, {countdown.minutes} minutes, {countdown.seconds} seconds"
    )
