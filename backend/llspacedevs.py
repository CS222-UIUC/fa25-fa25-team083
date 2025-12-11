import requests
import json
from collections import Counter
import os


class AstronautData:
    """
    Class for fetching and analyzing astronaut data from TheSpaceDevs API.
    Uses caching to avoid rate limiting, which was the solution I found when I looked up my issue
    """

    def __init__(
        self,
        cache_file="astronauts.json",
        base_url="https://lldev.thespacedevs.com/2.2.0/astronaut/",
    ):
        self.cache_file = cache_file
        self.base_url = base_url
        self._astronauts = None

    def _fetch_astronauts(self):
        """
        Fetch astronauts from API with caching.
        Returns a list of astronaut dictionaries.
        """
        # if cache exists, retun
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "r") as f:
                return json.load(f)

        # Fetch from API
        astronauts = []
        url = f"{self.base_url}?limit=100"

        # Adapted this code from another project I am working on and used AI to tailor it and get the exception raising
        while url:
            print(f"Fetching: {url}")
            r = requests.get(url)

            if r.status_code == 429:
                raise Exception("Rate limit hit — try again later or use caching.")

            r.raise_for_status()
            data = r.json()
            astronauts.extend(data.get("results", []))
            url = data.get("next")

        # Save to cache
        with open(self.cache_file, "w") as f:
            json.dump(astronauts, f, indent=2)

        return astronauts

    def get_astronauts(self):
        """
        Get all astronauts (cached after first fetch).
        Returns a list of astronaut dictionaries. These dictionaries contain the astronaut's name, nationality.
        """
        if self._astronauts is None:
            self._astronauts = self._fetch_astronauts()
        return self._astronauts

    def get_astronauts_by_country(self, country_name):
        """
         Get astronaut names filtered by country.

        Takes in country name and returns list of astronauts from that country

        """
        astronauts = self.get_astronauts()

        filtered = [
            a["name"]
            for a in astronauts
            if a.get("nationality")
            and country_name.lower() in a.get("nationality", "").lower()
        ]

        return filtered

    def get_top_countries(self, top_n=10):
        """
        Get top N countries by astronaut count.

        Args:
            top_n: Number of top countries to return

        Returns:
            List of tuples: (country, count, [astronaut_names])
        """
        astronauts = self.get_astronauts()

        # Collect astronauts per nationality with status
        nationality_counts = Counter()
        nationality_astronauts = {}

        for astronaut in astronauts:
            nationality = astronaut.get("nationality")
            status = (astronaut.get("status") or {}).get("name")
            if nationality:
                nationality_counts[nationality] += 1
                if nationality not in nationality_astronauts:
                    nationality_astronauts[nationality] = []
                nationality_astronauts[nationality].append(
                    {"name": astronaut.get("name"), "status": status}
                )

        # Get top N countries
        top_countries = nationality_counts.most_common(top_n)

        # Return with astronaut names split into active/inactive lists
        result = []
        for country, count in top_countries:
            people = nationality_astronauts.get(country, [])
            active = [p["name"] for p in people if (p.get("status") or "").lower() == "active"]
            inactive = [p["name"] for p in people if (p.get("status") or "").lower() != "active"]
            result.append((country, count, {"active": active, "inactive": inactive}))
        return result

    def get_astronaut_count_by_country(self):
        """
        Get astronaut count for each country.

        Returns:
            Dictionary mapping country names to astronaut counts
        """
        astronauts = self.get_astronauts()

        nationality_counts = Counter()
        for astronaut in astronauts:
            nationality = astronaut.get("nationality")
            if nationality:
                nationality_counts[nationality] += 1

        return dict(nationality_counts)


def main():
    """Example usage of the AstronautData class."""
    astronaut_data = AstronautData()

    # Example 1: Get top 10 countries
    print("Top 10 countries by astronaut count:\n")
    top_countries = astronaut_data.get_top_countries(10)
    for i, (country, count, names) in enumerate(top_countries, 1):
        print(f"{i}. {country}: {count} astronaut(s)")
        for name in names:
            print(f"   - {name}")
        print()

    # Example 2: Get astronauts by country
    print("\n" + "=" * 60)
    print("American astronauts:")
    americans = astronaut_data.get_astronauts_by_country("American")
    for name in americans:
        print(f"  - {name}")

    # Example 3: Get all country counts
    print("\n" + "=" * 60)
    print("All countries with astronaut counts:")
    all_counts = astronaut_data.get_astronaut_count_by_country()
    for country, count in sorted(all_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {country}: {count}")
    # Print this to see all the fields that an astronaut has in case you are curious
    # for astronaut in astronaut_data.get_astronauts():
    #     print(astronaut)
    #     print("")


if __name__ == "__main__":
    main()
