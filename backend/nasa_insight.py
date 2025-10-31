import nasa_apod  # For getNASA_APIKey():
import requests
import os
import time
import json

INSIGHT_URL = "https://api.nasa.gov/insight_weather/"
CACHE_PATH = os.path.join(os.path.dirname(__file__), "insight_cache.json") #should be cached in /backend

def load_cached_data():
    """
    Got help from GPT to reduce and cache the amount of calls using the API.
    Try to read previously fetched InSight data from disk.
    Returns a dictionary. Otherwise will return None.
    """
    if not os.path.exists(CACHE_PATH):
        return None

    try:
        with open(CACHE_PATH, "r", encoding = "utf-8") as f:
            cached = json.load(f)
        if time.time() - cached.get("ts", 0) > (60 * 10): #(60 * 10) is 60 seconds * 10 for 10 minutes
            return None #cache is old
        return cached.get("data")
    except Exception:
        return None

def fetch_insight_api():
    """
    Got help from GPT to reduce and cache the amount of calls using the API.
    Fetch fresh data from the NASA InSight endpoint and write it to disk.
    Returns a dictionary. Otherwise None
    """
    resp = requests.get(
        INSIGHT_URL,
        params = {
            "api_key": nasa_apod.getNASA_APIKey(),
            "feedtype": "json",
            "ver": "1.0",

        },
        timeout = 10,
    )
    resp.raise_for_status()
    data = resp.json()
    try: 
        with open(CACHE_PATH, "w", encoding = "utf-8") as f:
            json.dump({"ts": time.time(), "data": data}, f)
    except Exception:
        pass #HAS TO BE PASS in case writing fails
    return data


def get_insight_data():
    """
    Got help from GPT to reduce and cache the amount of calls using the API.
    Main entry for InSight data. Will be used for basically all getters
    Returns a dictionary. Otherwise None
    """
    data = load_cached_data()
    if data is not None:
        return data
    
    try: 
        return fetch_insight_api()
    except Exception:
        return {}
    


def get_sols():
    """
    Returns a list of strings with sols.
    A sol is a Martian day
    https://api.nasa.gov/assets/insight/InSight%20Weather%20API%20Documentation.pdf
    Based on the API, the call will return the most recent sol days and each sol day
    is a key for future references. As such, you'll want to call the max() of the list
    as that will be the recent sol day.
    """
    data = get_insight_data()
    return list(data.get("sol_keys", []))


def get_latest_sol():
    """
    Using the get_sols() function to return the max int of the sols.
    Essentially returning the most recent sol day according to the API.
    """
    sols = get_sols()
    return max(sols)


def get_temp_avg():
    """
    Getting average temp for the latest sol day.
    Should be celsius
    Returns none if not present
    """
    data = get_insight_data()
    latest = get_latest_sol()

    ls = data.get(str(latest), {}) # The keys in the json file are strings
    at = ls.get("AT")
    if not at or "av" not in at:
        return None 
    return float(at["av"])
   
    
def get_temp_min():
    """
    Getting min temp for the latest sol day.
    Should be in celsius
    Returns none if not present
    """
    data = get_insight_data()
    latest = get_latest_sol()

    ls = data.get(str(latest), {}) # The keys in the json file are strings
    at = ls.get("AT")
    if not at or "mn" not in at:
        return None 
    return float(at["mn"])

  
        
def get_temp_max():
    """
    Getting max temp for the latest sol day.
    Should be in celsius
    Returns none if not present
    """
    data = get_insight_data()
    latest = get_latest_sol()

    ls = data.get(str(latest), {}) # The keys in the json file are strings
    at = ls.get("AT")
    if not at or "mx" not in at:
        return None 
    return float(at["mx"])

    

def get_wind_avg():
    """
    Getting average wind for the latest sol day. Should be in m/s.
    We can later implement backend helpers to convert if necessary otherwise front end can convert if needed
    Returns none if not present
    """
    data = get_insight_data()
    latest = get_latest_sol()

    ls = data.get(str(latest), {}) # The keys in the json file are strings
    hws = ls.get("HWS")
    if not hws or "av" not in hws:
        return None 
    return float(hws["av"])

   
def get_wind_min():
    """
    Getting min wind for the latest sol day. Should be in m/s.
    Returns none if not present
    """
    data = get_insight_data()
    latest = get_latest_sol()

    ls = data.get(str(latest), {}) # The keys in the json file are strings
    hws = ls.get("HWS")
    if not hws or "mn" not in hws:
        return None 
    return float(hws["mn"])


    
def get_wind_max():
    """
    Getting max wind for the latest sol day. Should be in m/s.
    Returns none if not present
    """
    data = get_insight_data()
    latest = get_latest_sol()

    ls = data.get(str(latest), {}) # The keys in the json file are strings
    hws = ls.get("HWS")
    if not hws or "mx" not in hws:
        return None 
    return float(hws["mx"])

def get_pressure_avg():
    """
    Return the average pressure in Pascals (Pa) for the given day
    """
    ls = get_insight_data()
    pre = ls.get("PRE")
    if not pre or "av" not in pre:
        return None
    return float(pre["av"])

def get_pressure_min():
    """
    Return the min pressure for the given day
    """
    ls = get_insight_data()
    pre = ls.get("PRE")
    if not pre or "mn" not in pre:
        return None
    return float(pre["mn"])

def get_pressure_max():
    """
    Return the max pressure for the given day
    """
    ls = get_insight_data()
    pre = ls.get("PRE")
    if not pre or "mx" not in pre:
        return None
    return float(pre["mx"])


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

    print("---------------")
    print(get_temp_max())
    print(get_temp_min())
    print("------------")
    print(get_wind_avg())
    print(get_wind_max())
    print(get_wind_min())


