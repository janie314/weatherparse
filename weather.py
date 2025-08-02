import requests

def get_weather_forecast():
    """
    Fetches weather forecast data from api.weather.gov, extracts and prints
    specific temperature information, and the short forecast.
    """
    url = "https://api.weather.gov/gridpoints/MKX/37,61/forecast"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        data = response.json()

        # 2. Prints the JSON node properties.periods[0].temperature and stores that in a variable temp
        temp_fahrenheit = data['properties']['periods'][0]['temperature']
        print(temp_fahrenheit, end="") # Using end="" to avoid newline

        # 3. Prints "°F/"
        print("°F/", end="")

        # 4. Converts temp to celsius and rounds to int
        temp_celsius = int((temp_fahrenheit - 32) * 5/9)

        # 5. Prints "°C"
        print(f"{temp_celsius}°C", end="")

        # 6. Prints the JSON node properties.periods[0].shortForecast
        short_forecast = data['properties']['periods'][0]['shortForecast']
        print(f" {short_forecast}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
    except KeyError as e:
        print(f"Error parsing JSON data: Missing key {e}")
    except IndexError as e:
        print(f"Error accessing forecast period: {e}")

if __name__ == "__main__":
    get_weather_forecast()
