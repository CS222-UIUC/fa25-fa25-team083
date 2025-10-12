import nasa_apod  # For getNASA_APIKey():
import requests


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
    sols = get_sols()
    return max(sols)


if __name__ == "__main__":
    """
    Testing function calls locally
    """

    sols = get_sols()
    print(sols)
    print()
    print(get_latest_sol())
