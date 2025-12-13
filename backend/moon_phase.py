"""Moon phase calculations and data.

Provides functions to calculate current moon phase, illumination percentage,
and next phase information using astronomical formulas.
Also includes moon rise/set times based on location.
"""

from __future__ import annotations

import math
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional

try:
    from skyfield.api import load, Topos
    from skyfield.almanac import find_discrete, risings_and_settings

    SKYFIELD_AVAILABLE = True
except ImportError:
    SKYFIELD_AVAILABLE = False


# Mean synodic month (new moon to new moon), in days.
_SYNODIC_MONTH = 29.530588853

# Reference new moon: 2000-01-06 18:14 UTC (Meeus), JD ≈ 2451550.1
# Using a well-known epoch greatly improves phase accuracy for simple models.
_NEW_MOON_EPOCH_JD = 2451550.1


def _to_utc(dt: datetime) -> datetime:
    """Return an aware UTC datetime. If naive, assume it's already UTC."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _julian_day(dt: datetime) -> float:
    """Compute Julian Day (JD) including fractional day, for Gregorian calendar dates."""
    dt = _to_utc(dt)

    y = dt.year
    m = dt.month
    d = dt.day

    # Fractional day from time (UTC)
    frac_day = (
        dt.hour + (dt.minute + (dt.second + dt.microsecond / 1_000_000) / 60.0) / 60.0
    ) / 24.0

    if m <= 2:
        y -= 1
        m += 12

    a = y // 100
    b = 2 - a + (a // 4)

    # Meeus: JD = floor(365.25*(y+4716)) + floor(30.6001*(m+1)) + d + b - 1524.5 + frac_day
    jd = (
        math.floor(365.25 * (y + 4716))
        + math.floor(30.6001 * (m + 1))
        + d
        + b
        - 1524.5
        + frac_day
    )
    return jd


def calculate_moon_phase(date: datetime) -> Dict[str, Any]:
    """Calculate moon phase information for a given date.

    Returns a dict with phase name, illumination percentage, age, and next phase info.
    """
    jd = _julian_day(date)

    # Days since a known new moon epoch.
    days_since_new = jd - _NEW_MOON_EPOCH_JD

    # Phase in [0, 1)
    phase = (days_since_new / _SYNODIC_MONTH) % 1.0

    # Moon age in days
    age = phase * _SYNODIC_MONTH

    # Illumination percentage (simple phase-geometry approximation)
    illumination = (1.0 - math.cos(2.0 * math.pi * phase)) / 2.0 * 100.0

    # Determine phase name + next major phase (New, First Quarter, Full, Last Quarter)
    # Boundaries at: 0.00, 0.25, 0.50, 0.75, 1.00
    if phase < 0.25:
        phase_name = "Waxing Crescent" if phase > 0.02 else "New Moon"
        next_phase = "First Quarter"
        next_boundary = 0.25
    elif phase < 0.50:
        phase_name = "Waxing Gibbous" if phase > 0.27 else "First Quarter"
        next_phase = "Full Moon"
        next_boundary = 0.50
    elif phase < 0.75:
        phase_name = "Waning Gibbous" if phase > 0.52 else "Full Moon"
        next_phase = "Last Quarter"
        next_boundary = 0.75
    else:
        phase_name = "Waning Crescent" if phase < 0.98 else "New Moon"
        next_phase = "New Moon"
        next_boundary = 1.00

    days_to_next = (next_boundary - phase) * _SYNODIC_MONTH
    if days_to_next < 0:
        days_to_next += _SYNODIC_MONTH

    return {
        "phase": phase_name,
        "illumination": round(illumination, 1),
        "age": round(age, 1),
        "next_phase": next_phase,
        "days_to_next": round(days_to_next, 1),
        "date": date.isoformat(),
    }


def get_current_moon_phase(
    latitude: Optional[float] = None, longitude: Optional[float] = None
) -> Dict[str, Any]:
    """Get current moon phase information."""
    now = datetime.now()
    phase_data = calculate_moon_phase(now)

    if latitude is not None and longitude is not None:
        rise_set = calculate_moon_rise_set(now, latitude, longitude)
        phase_data.update(rise_set)

    return phase_data


def get_moon_phase_for_date(
    date_str: str, latitude: Optional[float] = None, longitude: Optional[float] = None
) -> Dict[str, Any]:
    """Get moon phase for a specific date (YYYY-MM-DD format)."""
    try:
        date = datetime.fromisoformat(date_str)
        phase_data = calculate_moon_phase(date)

        if latitude is not None and longitude is not None:
            rise_set = calculate_moon_rise_set(date, latitude, longitude)
            phase_data.update(rise_set)

        return phase_data
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")


def get_moon_phase_range(start_date: str, days: int = 7) -> list[Dict[str, Any]]:
    """Get moon phase information for a range of dates."""
    try:
        start = datetime.fromisoformat(start_date)
        phases = []

        for i in range(days):
            current_date = start + timedelta(days=i)
            phases.append(calculate_moon_phase(current_date))

        return phases
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")


def calculate_moon_rise_set(
    date: datetime, latitude: float, longitude: float
) -> Dict[str, Any]:
    """Calculate moon rise and set times for a specific location and date.

    Returns a dict with rise and set times, or None if the moon doesn't rise/set.
    """
    if not SKYFIELD_AVAILABLE:
        return {"error": "Skyfield library not available for rise/set calculations"}

    try:
        # Load ephemeris
        eph = load("de421.bsp")
        moon = eph["moon"]

        # Create location
        location = Topos(latitude_degrees=latitude, longitude_degrees=longitude)

        # Time scale
        ts = load.timescale()

        # Get times for the date
        start_time = ts.utc(date.year, date.month, date.day, 0, 0, 0)
        end_time = ts.utc(date.year, date.month, date.day, 23, 59, 59)

        # Find rise and set times
        f = risings_and_settings(eph, moon, location)
        times, events = find_discrete(start_time, end_time, f)

        rise_time = None
        set_time = None

        for t, event in zip(times, events):
            if event == 1:  # Rising
                rise_time = t.utc_datetime()
            elif event == 0:  # Setting
                set_time = t.utc_datetime()

        return {
            "rise": rise_time.isoformat() if rise_time else None,
            "set": set_time.isoformat() if set_time else None,
            "location": {"lat": latitude, "lon": longitude},
        }

    except Exception as e:
        return {"error": f"Failed to calculate rise/set times: {str(e)}"}
