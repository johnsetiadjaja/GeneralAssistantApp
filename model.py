import requests


class WeatherModel:
    def __init__(self):
        self.weather_codes = {
            0: ("Clear sky", "☀️"),
            1: ("Mainly clear", "🌤️"), 2: ("Partly cloudy", "⛅"), 3: ("Overcast", "☁️"),
            45: ("Fog", "🌫️"), 48: ("Depositing rime fog", "🌫️"),
            51: ("Light drizzle", "🌧️"), 53: ("Moderate drizzle", "🌧️"), 55: ("Dense drizzle", "🌧️"),
            61: ("Slight rain", "🌦️"), 63: ("Moderate rain", "🌧️"), 65: ("Heavy rain", "🌧️"),
            71: ("Slight snow", "🌨️"), 73: ("Moderate snow", "❄️"), 75: ("Heavy snow", "❄️"),
            80: ("Rain showers", "🌦️"), 81: ("Moderate showers", "🌧️"), 82: ("Violent showers", "⛈️"),
            95: ("Thunderstorm", "🌩️"), 96: ("Thunderstorm + hail", "⛈️"), 99: ("Heavy thunderstorm", "⛈️"),
        }

    def fetch_weather(self, city_name):
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"

        try:
            geo_response = requests.get(geo_url, timeout=5)
            geo_data = geo_response.json()

            if "results" not in geo_data or len(geo_data["results"]) == 0:
                return False, f"City '{city_name}' not found. Please check spelling."

            location = geo_data["results"][0]
            lat = location["latitude"]
            lon = location["longitude"]
            country = location.get("country", "")
            resolved_city = f"{location['name']}, {country}".strip(", ")
            timezone_str = location.get("timezone", "UTC")

            # Step 2: Fetch weather using exact parameters
            weather_url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={lat}&longitude={lon}&"
                f"current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m"
            )

            weather_response = requests.get(weather_url, timeout=5)
            weather_data = weather_response.json()

            # Helpful debug print to see what the API actually returned if it fails
            if "current" not in weather_data:
                print("API Error Response:", weather_data)
                reason = weather_data.get("reason", "Unknown API error format.")
                return False, f"API Error: {reason}"

            current = weather_data["current"]
            code = current.get("weather_code", 0)
            desc, emoji = self.weather_codes.get(code, ("Unknown Weather", "❓"))

            weather_package = {
                "city": resolved_city,
                "temp": current.get("temperature_2m", 0),
                "feels_like": current.get("apparent_temperature", 0),
                "humidity": current.get("relative_humidity_2m", 0),
                "wind_speed": current.get("wind_speed_10m", 0),
                "desc": desc,
                "emoji": emoji,
                "timezone": timezone_str
            }

            return True, weather_package

        except requests.exceptions.RequestException:
            return False, "Network error! Please check your internet connection."
        except Exception as e:
            return False, f"An unexpected error occurred: {e}"