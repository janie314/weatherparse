import argparse
import os
import json
import requests
import datetime


def display_weather_forecast(cache_path, cache_timeout, weather_gov):
    """
    Fetches weather forecast data from api.weather.gov, extracts and prints
    specific temperature information, and the short forecast.
    """
    if os.path.exists(cache_path):
        last_modified = os.path.getmtime(cache_path)
        age = datetime.now().timestamp() - last_modified
        if age < float(cache_timeout):
            with open(cache_path) as cache:
                print(json.load(cache))

    url = f"https://api.weather.gov/gridpoints/{weather_gov}/forecast"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        data = response.json()

        # 2. Prints the JSON node properties.periods[0].temperature and stores that in a variable temp
        temp_fahrenheit = data["properties"]["periods"][0]["temperature"]
        res = f"{temp_fahrenheit}°F/"

        # 4. Converts temp to celsius and rounds to int
        temp_celsius = int((temp_fahrenheit - 32) * 5 / 9)

        # 5. Prints "°C"
        res += f"{temp_celsius}°C"

        # 6. Prints the JSON node properties.periods[0].shortForecast
        short_forecast = data["properties"]["periods"][0]["shortForecast"]
        res += f" {short_forecast}"

        print(res)

        with open(cache_path, "w") as cache:
            json.dump(res, cache)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
    except KeyError as e:
        print(f"Error parsing JSON data: Missing key {e}")
    except IndexError as e:
        print(f"Error accessing forecast period: {e}")


def read_config(config_path):
    with open(config_path) as config:
        return json.load(config)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        prog="weatherparse", description="Prints weather data."
    )
    homedir = os.environ.get("HOME")
    argparser.add_argument(
        "-c",
        "--cache",
        help="cache file of calendar state (default $HOME/.cache/weatherparse-cache.json)",
        default=os.path.join(homedir, ".cache/weatherparse-cache.json"),
    )
    argparser.add_argument(
        "--cache_timeout",
        help="length of time the cache is good for (seconds, default: 3600)",
        default=3600,
    )
    argparser.add_argument(
        "--weather_gov",
        help="URL segment for api.weather.gov (default: 'MKX/37,61')",
        default="MKX/37,61",
    )
    args = argparser.parse_args()
    display_weather_forecast(args.cache, args.cache_timeout, args.weather_gov)
