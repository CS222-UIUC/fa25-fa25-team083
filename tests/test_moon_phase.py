import os
import sys
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock

# Add the project root to the Python path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import pytest
from backend.moon_phase import (
    calculate_moon_phase,
    get_current_moon_phase,
    get_moon_phase_for_date,
    get_moon_phase_range,
    calculate_moon_rise_set,
    _julian_day,
    _to_utc,
    _SYNODIC_MONTH,
    _NEW_MOON_EPOCH_JD,
    SKYFIELD_AVAILABLE,
)


class TestMoonPhaseCalculations:
    """Test basic moon phase calculations without external dependencies."""

    def test_julian_day_known_date(self):
        """Test Julian Day calculation for a known date."""
        # 2023-01-01 12:00:00 UTC should be JD 2459946.0
        dt = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        jd = _julian_day(dt)
        expected_jd = 2459946.0
        assert abs(jd - expected_jd) < 0.001

    def test_to_utc_naive_datetime(self):
        """Test _to_utc with naive datetime."""
        dt = datetime(2023, 1, 1, 12, 0, 0)
        utc_dt = _to_utc(dt)
        assert utc_dt.tzinfo == timezone.utc
        assert utc_dt.hour == 12

    def test_to_utc_aware_datetime(self):
        """Test _to_utc with already aware datetime."""
        dt = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        utc_dt = _to_utc(dt)
        assert utc_dt == dt

    def test_calculate_moon_phase_new_moon(self):
        """Test moon phase calculation for a known new moon date."""
        # Approximate new moon date
        dt = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        result = calculate_moon_phase(dt)

        assert isinstance(result, dict)
        assert "phase" in result
        assert "illumination" in result
        assert "age" in result
        assert "next_phase" in result
        assert "days_to_next" in result
        assert "date" in result

        assert isinstance(result["illumination"], float)
        assert 0 <= result["illumination"] <= 100
        assert isinstance(result["age"], float)
        assert 0 <= result["age"] < _SYNODIC_MONTH
        assert isinstance(result["days_to_next"], float)

    def test_calculate_moon_phase_full_moon(self):
        """Test moon phase calculation for a date with high illumination."""
        # Date with high illumination (near full moon)
        dt = datetime(2023, 1, 6, 12, 0, 0, tzinfo=timezone.utc)
        result = calculate_moon_phase(dt)

        assert isinstance(result, dict)
        assert "phase" in result
        assert result["illumination"] > 95  # Should be nearly full

    def test_get_moon_phase_for_date_valid(self):
        """Test get_moon_phase_for_date with valid date string."""
        result = get_moon_phase_for_date("2023-01-01")

        assert isinstance(result, dict)
        assert "phase" in result
        assert "date" in result

    def test_get_moon_phase_for_date_invalid(self):
        """Test get_moon_phase_for_date with invalid date string."""
        with pytest.raises(ValueError, match="Invalid date format"):
            get_moon_phase_for_date("invalid-date")

    def test_get_moon_phase_range(self):
        """Test get_moon_phase_range function."""
        result = get_moon_phase_range("2023-01-01", days=3)

        assert isinstance(result, list)
        assert len(result) == 3
        for phase_data in result:
            assert isinstance(phase_data, dict)
            assert "phase" in phase_data

    def test_get_moon_phase_range_invalid_date(self):
        """Test get_moon_phase_range with invalid date."""
        with pytest.raises(ValueError, match="Invalid date format"):
            get_moon_phase_range("invalid-date")

    @patch("backend.moon_phase.datetime")
    def test_get_current_moon_phase(self, mock_datetime):
        """Test get_current_moon_phase function."""
        mock_datetime.now.return_value = datetime(
            2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc
        )

        result = get_current_moon_phase()

        assert isinstance(result, dict)
        assert "phase" in result
        mock_datetime.now.assert_called_once()


class TestMoonPhaseWithLocation:
    """Test moon phase functions that include location-based calculations."""

    @patch("backend.moon_phase.calculate_moon_rise_set")
    def test_get_current_moon_phase_with_location(self, mock_rise_set):
        """Test get_current_moon_phase with location parameters."""
        mock_rise_set.return_value = {
            "rise": "2023-01-01T18:00:00",
            "set": "2023-01-01T06:00:00",
            "location": {"lat": 40.0, "lon": -74.0},
        }

        result = get_current_moon_phase(latitude=40.0, longitude=-74.0)

        assert isinstance(result, dict)
        assert "rise" in result
        assert "set" in result
        assert "location" in result
        mock_rise_set.assert_called_once()

    @patch("backend.moon_phase.calculate_moon_rise_set")
    def test_get_moon_phase_for_date_with_location(self, mock_rise_set):
        """Test get_moon_phase_for_date with location parameters."""
        mock_rise_set.return_value = {
            "rise": "2023-01-01T18:00:00",
            "set": "2023-01-01T06:00:00",
            "location": {"lat": 40.0, "lon": -74.0},
        }

        result = get_moon_phase_for_date("2023-01-01", latitude=40.0, longitude=-74.0)

        assert isinstance(result, dict)
        assert "rise" in result
        assert "set" in result
        assert "location" in result
        mock_rise_set.assert_called_once()


@pytest.mark.skipif(not SKYFIELD_AVAILABLE, reason="Skyfield library not available")
class TestMoonRiseSetCalculations:
    """Test moon rise/set calculations (requires Skyfield)."""

    @patch("backend.moon_phase.load")
    def test_calculate_moon_rise_set_success(self, mock_load):
        """Test successful moon rise/set calculation."""
        # Mock Skyfield objects
        mock_eph = MagicMock()
        mock_moon = MagicMock()
        mock_eph.__getitem__.return_value = mock_moon

        mock_ts = MagicMock()
        mock_times = MagicMock()
        mock_events = MagicMock()

        # Mock the find_discrete function
        with patch(
            "backend.moon_phase.find_discrete", return_value=(mock_times, mock_events)
        ) as mock_find_discrete, patch(
            "backend.moon_phase.risings_and_settings"
        ) as mock_risings:

            # Setup mock times and events
            mock_time1 = MagicMock()
            mock_time1.utc_datetime.return_value = datetime(
                2023, 1, 1, 18, 0, 0, tzinfo=timezone.utc
            )
            mock_time2 = MagicMock()
            mock_time2.utc_datetime.return_value = datetime(
                2023, 1, 1, 6, 0, 0, tzinfo=timezone.utc
            )

            mock_times.__iter__.return_value = [mock_time1, mock_time2]
            mock_events.__iter__.return_value = [1, 0]  # 1 = rise, 0 = set

            mock_load.return_value = mock_eph
            mock_load.timescale.return_value = mock_ts

            dt = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
            result = calculate_moon_rise_set(dt, 40.0, -74.0)

            assert isinstance(result, dict)
            assert "rise" in result
            assert "set" in result
            assert "location" in result
            assert result["location"]["lat"] == 40.0
            assert result["location"]["lon"] == -74.0

    def test_calculate_moon_rise_set_no_skyfield(self):
        """Test moon rise/set calculation when Skyfield is not available."""
        with patch("backend.moon_phase.SKYFIELD_AVAILABLE", False):
            dt = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
            result = calculate_moon_rise_set(dt, 40.0, -74.0)

            assert isinstance(result, dict)
            assert "error" in result
            assert "Skyfield library not available" in result["error"]

    @patch("backend.moon_phase.load")
    def test_calculate_moon_rise_set_exception(self, mock_load):
        """Test moon rise/set calculation when an exception occurs."""
        mock_load.side_effect = Exception("Test error")

        dt = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        result = calculate_moon_rise_set(dt, 40.0, -74.0)

        assert isinstance(result, dict)
        assert "error" in result
        assert "Test error" in result["error"]


class TestMoonPhaseConstants:
    """Test moon phase constants and mathematical relationships."""

    def test_synodic_month_constant(self):
        """Test that the synodic month constant is reasonable."""
        assert 29.5 < _SYNODIC_MONTH < 29.6

    def test_new_moon_epoch(self):
        """Test that the new moon epoch JD is reasonable."""
        # JD should be around 2451550 for year 2000
        assert 2451500 < _NEW_MOON_EPOCH_JD < 2451600

    def test_phase_continuity(self):
        """Test that moon phase calculations are continuous."""
        dt1 = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        dt2 = datetime(2023, 1, 2, 12, 0, 0, tzinfo=timezone.utc)

        phase1 = calculate_moon_phase(dt1)
        phase2 = calculate_moon_phase(dt2)

        # Phase should increase by approximately 1/_SYNODIC_MONTH
        expected_diff = 1.0 / _SYNODIC_MONTH
        actual_diff = (phase2["age"] - phase1["age"]) / 24.0  # Convert to days

        # Allow some tolerance due to calculation precision
        assert abs(actual_diff - expected_diff) < 0.01


class TestMoonPhaseEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_leap_year_date(self):
        """Test moon phase calculation for February 29 in a leap year."""
        dt = datetime(2024, 2, 29, 12, 0, 0, tzinfo=timezone.utc)
        result = calculate_moon_phase(dt)

        assert isinstance(result, dict)
        assert "phase" in result

    def test_year_boundary(self):
        """Test moon phase calculation near year boundary."""
        dt = datetime(2022, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
        result = calculate_moon_phase(dt)

        assert isinstance(result, dict)
        assert "phase" in result

    def test_moon_phase_range_single_day(self):
        """Test get_moon_phase_range with days=1."""
        result = get_moon_phase_range("2023-01-01", days=1)

        assert isinstance(result, list)
        assert len(result) == 1

    def test_moon_phase_range_large_range(self):
        """Test get_moon_phase_range with larger date range."""
        result = get_moon_phase_range("2023-01-01", days=10)

        assert isinstance(result, list)
        assert len(result) == 10

        # Check that dates are consecutive
        for i in range(1, len(result)):
            prev_date = datetime.fromisoformat(result[i - 1]["date"])
            curr_date = datetime.fromisoformat(result[i]["date"])
            assert (curr_date - prev_date).days == 1
