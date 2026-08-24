"""
Gujarat SmartGuide AI — Charts & Visualization Module
Provides chart data preparation functions for Streamlit/Plotly rendering.
"""

import json
import os

def get_population_chart_data() -> dict:
    """Return population data for all locations (for bar chart)."""
    data_path = os.path.join(os.path.dirname(__file__), "gujarat_locations.json")
    with open(data_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    locs = sorted(raw["locations"], key=lambda x: x["population"], reverse=True)
    return {
        "names": [l["name"] for l in locs],
        "populations": [l["population"] for l in locs],
        "districts": [l["district"] for l in locs],
        "types": [l["type"] for l in locs],
    }


def get_district_count_data() -> dict:
    """Return count of locations per district."""
    data_path = os.path.join(os.path.dirname(__file__), "gujarat_locations.json")
    with open(data_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    district_counts: dict[str, int] = {}
    for loc in raw["locations"]:
        d = loc["district"]
        district_counts[d] = district_counts.get(d, 0) + 1
    sorted_d = sorted(district_counts.items(), key=lambda x: x[1], reverse=True)
    return {
        "districts": [item[0] for item in sorted_d],
        "counts": [item[1] for item in sorted_d],
    }


def get_weather_comparison_data() -> dict:
    """Return temperature and humidity comparison across locations."""
    data_path = os.path.join(os.path.dirname(__file__), "gujarat_locations.json")
    with open(data_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    locs = raw["locations"]
    return {
        "names": [l["name"] for l in locs],
        "temperatures": [l["weather"]["temperature_c"] for l in locs],
        "humidity": [l["weather"]["humidity_percent"] for l in locs],
        "rain_chance": [l["weather"]["rain_chance_percent"] for l in locs],
    }
