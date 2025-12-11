"""Helpers for NASA NEO (Near Earth Object) API.

Provides functions to call the NEO feed, lookup and browse endpoints and
produce a compact summary useful for the dashboard.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, Optional

import requests

import nasa_apod


API_BASE = "https://api.nasa.gov/neo/rest/v1"


def _api_key() -> str:
    return nasa_apod.getNASA_APIKey()


def fetch_feed(start_date: str, end_date: str) -> Dict[str, Any]:
    """Fetch NEO feed for a date range (max 7 days).

    start_date and end_date are ISO date strings YYYY-MM-DD.
    Returns parsed JSON from the NASA API.
    """
    url = f"{API_BASE}/feed"
    params = {"start_date": start_date, "end_date": end_date, "api_key": _api_key()}
    resp = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()


def summarize_feed(feed_json: Dict[str, Any]) -> Dict[str, Any]:
    """Produce a compact summary from feed JSON.

    Returns dict with keys: element_count, closest (dict), largest (dict).
    """
    element_count = int(feed_json.get("element_count") or 0)
    neos = feed_json.get("near_earth_objects", {}) or {}
    closest: Optional[Dict[str, Any]] = None
    largest: Optional[Dict[str, Any]] = None

    # collect candidate close approaches so we can return a top-N list
    close_approaches: list[Dict[str, Any]] = []
    # flattened list of all NEOs for the requested date range
    all_neos: list[Dict[str, Any]] = []

    for date_str, items in neos.items():
        for obj in items:
            nid = obj.get("id")
            name = obj.get("name")

            # estimated diameter (meters)
            try:
                diam = (
                    obj.get("estimated_diameter", {}).get("meters", {}).get("estimated_diameter_max")
                )
                diam = float(diam) if diam is not None else None
            except Exception:
                diam = None

            if diam is not None:
                if largest is None or diam > (largest.get("max_diameter_m") or 0):
                    largest = {"id": nid, "name": name, "max_diameter_m": diam}

            # close approach data - use first entry if present
            cad = obj.get("close_approach_data") or []
            first = cad[0] if cad else None
            miss_km = None
            vel_kms = None
            close_date = None
            if first:
                try:
                    miss_km = float(first.get("miss_distance", {}).get("kilometers"))
                except Exception:
                    miss_km = None
                try:
                    vel_kms = float(first.get("relative_velocity", {}).get("kilometers_per_second"))
                except Exception:
                    vel_kms = None
                close_date = first.get("close_approach_date")

            # build a flattened record for this object (include miss/vel if present)
            record = {
                "id": nid,
                "name": name,
                "close_date": close_date,
                "miss_distance_km": miss_km,
                "velocity_km_s": vel_kms,
            }
            all_neos.append(record)

            if miss_km is not None:
                # track single closest
                if closest is None or miss_km < (closest.get("miss_distance_km") or float("inf")):
                    closest = {
                        "id": nid,
                        "name": name,
                        "miss_distance_km": miss_km,
                        "velocity_km_s": vel_kms,
                        "close_date": close_date,
                    }

                # also append to list for top-N selection
                close_approaches.append(
                    {
                        "id": nid,
                        "name": name,
                        "miss_distance_km": miss_km,
                        "velocity_km_s": vel_kms,
                        "close_date": close_date,
                    }
                )

    # sort close approaches by miss distance ascending and take top 5
    closest_list = []
    try:
        closest_list = sorted(
            [c for c in close_approaches if c.get("miss_distance_km") is not None],
            key=lambda x: float(x.get("miss_distance_km")),
        )[:5]
    except Exception:
        closest_list = close_approaches[:5]

    return {
        "element_count": element_count,
        "closest": closest or {},
        "largest": largest or {},
        "closest_list": closest_list,
        "all_neos": all_neos,
    }


def get_neo_lookup(neo_id: str) -> Dict[str, Any]:
    url = f"{API_BASE}/neo/{neo_id}"
    params = {"api_key": _api_key()}
    resp = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()


def browse_neos(page: int = 0) -> Dict[str, Any]:
    url = f"{API_BASE}/neo/browse"
    params = {"api_key": _api_key(), "page": page}
    resp = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()
