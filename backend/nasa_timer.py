import datetime
from dataclasses import dataclass

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
        
        if target_time.tzinfo is None or target_time.tzinfo.utcoffset(target_time) is None:
            target_time = target_time.replace(tzinfo=datetime.timezone.utc)

        time_difference = target_time - current_time
        total_seconds = int(time_difference.total_seconds())

        if total_seconds < 0:
            return CountdownResult(target_name, target_datetime_str, 0, 0, 0, 0)
        
        days = total_seconds // (24 * 3600)
        seconds_remaining = total_seconds % (24 * 3600)
        hours = seconds_remaining // 3600
        minutes = (seconds_remaining % 3600) // 60
        seconds = (seconds_remaining % 60)
        
        return CountdownResult(
            target_name=target_name,
            target_date=target_datetime_str,
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds
        )
    except Exception:
        return CountdownResult(target_name, target_datetime_str, 0, 0, 0, 0)

# example
if __name__ == "__main__":
    target = "2025-09-01T10:00:00"
    countdown = get_countdown("Artemis II Launch", target)
    print(f"Countdown for {countdown.target_name}:")
    print(f"{countdown.days} days, {countdown.hours} hours, {countdown.minutes} minutes, {countdown.seconds} seconds")