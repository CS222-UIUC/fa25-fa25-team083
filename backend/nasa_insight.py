import nasa_apod  # For getNASA_APIKey():
import requests

base_url = "https://api.nasa.gov/insight_weather/"

def get_sols():
    """
    Returns a list of strings with sols.
    A sol is a Martian day
    https://api.nasa.gov/assets/insight/InSight%20Weather%20API%20Documentation.pdf
    Based on the API, the call will return the most recent sol days and each sol day
    is a key for future references. As such, you'll want to call the max() of the list
    as that will be the recent sol day.
    """
    try:
        resp = requests.get(
            "https://api.nasa.gov/insight_weather/",  # endpoint !!Might have to store this globally later for ease of access
            params={
                "api_key": nasa_apod.getNASA_APIKey(),
                "feedtype": "json",
                "ver": "1.0",
            },
            timeout=10,
        )

        resp.raise_for_status()
        data = resp.json()
        return list(data.get("sol_keys", []))  # return list of sols
    except Exception:
        return []  # return an empty list


def get_latest_sol():
    """
    Using the get_sols() function to return the max int of the sols.
    Essentially returning the most recent sol day according to the API.
    """
    if not get_sols():
        return None
    return max(get_sols(), key=int)


def get_temp_avg():
    """
    Getting average temp for the latest sol day.
    Should be celsius
    Returns none if not present
    """
    try:  # Doing a try and except just in case parsing fails in these function calls
        resp = requests.get(
            "https://api.nasa.gov/insight_weather/",
            params={
                "api_key": nasa_apod.getNASA_APIKey(),
                "feedtype": "json",
                "ver": "1.0",
            },
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()

        sols = data.get("sol_keys", [])
        if not sols:
            return None

        latest = get_latest_sol()

        at = data.get(latest, {}).get("AT")
        if not at or "av" not in at:
            return None
        return float(at["av"])
    except Exception:
        return None


def get_wind_avg():
    """
    Getting average wind for the latest sol day. Should be in m/s.
    We can later implement backend helpers to convert if necessary otherwise front end can convert if needed
    Returns none if not present
    """
    try:
        resp = requests.get(
            "https://api.nasa.gov/insight_weather/",
            params={
                "api_key": nasa_apod.getNASA_APIKey(),
                "feedtype": "json",
                "ver": "1.0",
            },
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()

        sols = data.get("sol_keys", [])
        if not sols:
            return None

        latest = get_latest_sol()
        if not latest:
            return None
        latest = str(latest)

        hws = data.get(latest, {}).get("HWS")
        if not hws or "av" not in hws:
            return None

        return float(hws["av"])
    except Exception:
        return None
    
def _fetch_insight():
    resp = requests.get(
        base_url,
        params={"api_key": nasa_apod.getNASA_APIKey(), "feedtype": "json", "ver": "1.0"},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()

def get_pressure_avg():
    try:
        data = _fetch_insight()
        sols = data.get("sol_keys", [])
        if not sols:
            return None
        latest = get_latest_sol()
        if not latest:
            return None
        pre = data.get(latest, {}).get("PRE")
        if not pre or "av" not in pre:
            return None
        return float(pre["av"])
    except Exception:
        return None


if __name__ == "__main__":
    """
    Testing function calls locally
    """

    sols = get_sols()
    print(sols)
    print()
    print(get_latest_sol())
    print(get_temp_avg())
    print(get_wind_avg())
