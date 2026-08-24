"""
Gujarat SmartGuide AI — Weather Service
==========================================
Currently uses MOCK/DEMO weather data embedded in the locations dataset.
This data is NOT real-time and is for demonstration purposes only.

─────────────────────────────────────────────────────────
HOW TO CONNECT A REAL WEATHER API (Future Enhancement)
─────────────────────────────────────────────────────────

Step 1: Sign up for a free weather API, e.g.:
        - OpenWeatherMap (https://openweathermap.org/api) — free tier available
        - WeatherAPI (https://www.weatherapi.com/) — free tier available

Step 2: Add your API key to the .env file:
        WEATHER_API_KEY=your_api_key_here
        WEATHER_API_URL=https://api.openweathermap.org/data/2.5/weather

Step 3: Replace the get_weather_for_location() function below with:
        def get_weather_for_location(location_name: str) -> dict:
            import requests
            api_key = os.getenv("WEATHER_API_KEY")
            url = f"{os.getenv('WEATHER_API_URL')}?q={location_name},IN&appid={api_key}&units=metric"
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            return {
                "condition": data["weather"][0]["description"].title(),
                "temperature_c": round(data["main"]["temp"]),
                "humidity_percent": data["main"]["humidity"],
                "wind_speed_kmh": round(data["wind"]["speed"] * 3.6),
                "feels_like_c": round(data["main"]["feels_like"]),
                "icon": "🌤️",   # map OWM icon codes to emojis
                "rain_chance_percent": 0,  # OWM free tier doesn't include this
                "source": "OpenWeatherMap (live)"
            }

Step 4: Remove the mock weather fallback.
─────────────────────────────────────────────────────────
"""

import os
from typing import Optional
from data.data_service import get_by_name, get_all_locations


# Weather condition to emoji mapping
CONDITION_ICONS = {
    "sunny": "☀️",
    "clear": "☀️",
    "hot": "🌡️",
    "hot and dry": "🌡️",
    "hot and humid": "🌤️",
    "partly cloudy": "⛅",
    "cloudy": "☁️",
    "overcast": "☁️",
    "rainy": "🌧️",
    "light rain": "🌦️",
    "heavy rain": "⛈️",
    "windy": "🌬️",
    "breezy": "🌊",
    "stormy": "⛈️",
    "foggy": "🌫️",
}


def get_condition_icon(condition: str) -> str:
    c = condition.lower()
    for key, icon in CONDITION_ICONS.items():
        if key in c:
            return icon
    return "🌡️"


def get_weather_for_location(location_name: str) -> Optional[dict]:
    """
    Retrieve mock weather data for a given location name.

    CURRENT SOURCE: Local JSON dataset (demo/mock data).
    To replace with live data — see module docstring above.
    """
    loc = get_by_name(location_name)
    if loc and "weather" in loc:
        w = loc["weather"].copy()
        w["location_name"] = loc["name"]
        w["district"] = loc["district"]
        w["source"] = "Demo dataset (not real-time)"
        w["icon"] = get_condition_icon(w.get("condition", ""))
        return w
    return None


def get_all_weather_data() -> list[dict]:
    """Return weather data for all locations (demo data)."""
    results = []
    for loc in get_all_locations():
        if "weather" in loc:
            w = loc["weather"].copy()
            w["location_name"] = loc["name"]
            w["district"] = loc["district"]
            w["icon"] = get_condition_icon(w.get("condition", ""))
            results.append(w)
    return results


def describe_weather(weather: dict) -> str:
    """Convert weather dict to a readable natural language description."""
    return (
        f"In **{weather['location_name']}** ({weather['district']} district), "
        f"the current demo weather shows **{weather['condition']}** conditions "
        f"with a temperature of **{weather['temperature_c']}°C** "
        f"(feels like {weather['feels_like_c']}°C). "
        f"Humidity is at **{weather['humidity_percent']}%**, "
        f"wind speed is **{weather['wind_speed_kmh']} km/h**, "
        f"and the chance of rain is **{weather['rain_chance_percent']}%**. "
        f"*(This is demo/mock data — not real-time weather.)*"
    )
