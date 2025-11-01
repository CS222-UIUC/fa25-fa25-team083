import os
import datetime
from dotenv import load_dotenv, find_dotenv
from dataclasses import dataclass
import requests


load_dotenv(
    find_dotenv(), override=False
)  # For loading the .env file and accessing any sensitive info like API keys - https://pypi.org/project/python-dotenv/


def getNASA_APIKey():
    """
    Return a NASA_API_KEY. If you have a valid .env key in your file, then you will return that key.
    Otherwise, yo uwill return NASA's default "DEMO_KEY" to still use methods.
    """
    key = os.getenv("NASA_API_KEY")

    if key:
        return key
    else:
        return "DEMO_KEY"


def getCurrDate():
    """
    Return a string of the current date in YYYY-MM-DD for APOD query
    https://stackoverflow.com/questions/3316882/how-do-i-get-a-string-format-of-the-current-date-time-in-python
    https://docs.python.org/3/library/datetime.html#format-codes
    """
    return datetime.date.today().strftime("%Y-%m-%d")
def today_date():
    """
    Return today's date as a datetime.date object
    """
    return datetime.date.today().strftime("%Y-%m-%d")


@dataclass
class APOD_Item:
    """
    https://docs.python.org/3/library/dataclasses.html
    """

    date: str
    title: str
    explanation: str
    media_type: str
    url: str
    hdurl: str
    copyright: str
    raw_url: str


def get_APOD() -> APOD_Item:
    """
    Will return an object on the current date.
    Otherwise, it will return an empty apod object of: {'date': '', 'title': '', 'explanation': '', 'media_type': '', 'url': '', 'hdurl': '', 'copyright': '', 'raw_url': ''}
    https://github.com/nasa/apod-api
    """

    api_key = getNASA_APIKey()
    today = getCurrDate()
    endpoint = "https://api.nasa.gov/planetary/apod"

    try:
        resp = requests.get(
            endpoint,
            params={"api_key": api_key, "date": today, "thumbs": "true"},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()  # Parse the JSON response into a dict
        if isinstance(data, dict) and "error" in data:
            return APOD_Item(
                "", "", "", "", "", "", "", ""
            )  # If there is an error return empty
    except Exception:  # any other error exception return empty
        return APOD_Item("", "", "", "", "", "", "", "")

    # print(f"Successfully fetched APOD for {today}")
    return APOD_Item(  # return the object
        date=data.get("date", ""),
        title=data.get("title", ""),
        explanation=data.get("explanation", ""),
        media_type=data.get("media_type", ""),
        url=data.get("thumbnail_url", data.get("url", "")),
        hdurl=data.get("hdurl"),
        copyright=data.get("copyright"),
        raw_url=data.get("url"),
    )
def get_APOD_for_date(date_str: str) -> APOD_Item:
    """
    Fetch APOD for a specific date ('YYYY-MM-DD').
    Returns empty item on any failure/invalid date.
    """
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return APOD_Item.empty()
    # @todo: finish this function


def get_APOD_lookback(max_lookback_days=30) -> APOD_Item:
    """
    Get NASA APOD from the last available day using a lookback parameter
    https://github.com/nasa/apod-api
    """
    api_key = getNASA_APIKey()
    today = datetime.date.today()
    endpoint = "https://api.nasa.gov/planetary/apod"

    def fetch(date_str: str):
        params = {"api_key": api_key, "date": date_str, "thumbs": "true"}
        return requests.get(
            endpoint, params=params, timeout=10
        )  # Makes HTTP Get with a timeout

    for d in range(
        max_lookback_days + 1
    ):  # Iterates each day starting from the current day and walks backwards until it reaches either a succesful day or the max_lookback_days
        date_obj = today - datetime.timedelta(days=d)
        date_str = date_obj.strftime("%Y-%m-%d")
        r = fetch(date_str)  # requests for the given date

        if not r.ok:
            if (
                r.status_code != 404
            ):  # A 404 means there is no nasa-apod that day and thus you can continue to traverse
                continue
            elif r.status_code == 429:  # A 429 means rate limited
                # print("Rate limited by the API.")
                break
            else:
                # print(f" {r.status_code} on {date_str}: {r.text[:200]}")
                continue

        data = r.json()  # parse json as a dict
        if "error" in data:  # Error with the API
            # print(f"NASA API error on {date_str}: {data['error'].get('message')}")
            break

        print(f"Successfully fetched APOD for {date_str}")
        return APOD_Item(
            date=data.get("date", ""),
            title=data.get("title", ""),
            explanation=data.get("explanation", ""),
            media_type=data.get("media_type", ""),
            url=data.get("thumbnail_url", data.get("url", "")),
            hdurl=data.get("hdurl"),
            copyright=data.get("copyright"),
            raw_url=data.get("url"),
        )

    # No data thus return empty object
    # print("Could not fetch any APOD data.")
    return APOD_Item("", "", "", "", "", "", "", "")

# local test
if __name__ == "__main__":
    apod = get_APOD()
    print(f"Today: {apod.date} | {apod.title} | media={apod.media_type}")
    # specific date
    y2k = get_APOD_for_date("2000-01-01")
    print(f"Y2K:{y2k.date} | {y2k.title}")