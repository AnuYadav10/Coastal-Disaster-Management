"""
Gujarat SmartGuide AI — Data Service
======================================
Loads and queries the local Gujarat locations dataset.
All data is DEMO/MOCK data — not real-time information.

To replace with a live database:
  - Replace load_data() with a database query
  - Ensure the returned dict structure matches the JSON schema
"""

import json
import os
from typing import Optional


# ─────────────────────────────────────────────
# Load Data
# ─────────────────────────────────────────────

def _data_path() -> str:
    return os.path.join(os.path.dirname(__file__), "gujarat_locations.json")


def load_data() -> list[dict]:
    """Load all locations from the local JSON file."""
    with open(_data_path(), "r", encoding="utf-8") as f:
        raw = json.load(f)
    return raw.get("locations", [])


_CACHE: list[dict] = []


def get_all_locations() -> list[dict]:
    """Return the full cached location list."""
    global _CACHE
    if not _CACHE:
        _CACHE = load_data()
    return _CACHE


# ─────────────────────────────────────────────
# Query Helpers
# ─────────────────────────────────────────────

def get_districts() -> list[str]:
    """Return sorted list of unique districts."""
    return sorted(set(loc["district"] for loc in get_all_locations()))


def get_by_district(district: str) -> list[dict]:
    """Return all locations in the given district (case-insensitive)."""
    d = district.strip().lower()
    return [loc for loc in get_all_locations() if loc["district"].lower() == d]


def search_locations(query: str) -> list[dict]:
    """
    Fuzzy search across name, district, taluka, and description.
    Returns locations sorted by relevance (name match first).
    """
    q = query.strip().lower()
    if not q:
        return []

    exact, partial, desc_match = [], [], []

    for loc in get_all_locations():
        name_l = loc["name"].lower()
        district_l = loc["district"].lower()
        desc_l = loc["description"].lower()
        taluka_l = loc.get("taluka", "").lower()

        if name_l == q:
            exact.append(loc)
        elif q in name_l or name_l in q:
            partial.append(loc)
        elif q in district_l or q in taluka_l:
            partial.append(loc)
        elif q in desc_l:
            desc_match.append(loc)

    return exact + partial + desc_match


def get_by_name(name: str) -> Optional[dict]:
    """Return a single location by exact name (case-insensitive)."""
    n = name.strip().lower()
    for loc in get_all_locations():
        if loc["name"].lower() == n:
            return loc
    return None


def get_top_by_population(n: int = 5) -> list[dict]:
    """Return top-N locations sorted by population descending."""
    return sorted(get_all_locations(), key=lambda x: x["population"], reverse=True)[:n]


def get_location_types() -> list[str]:
    """Return unique location types (city, town, village)."""
    return sorted(set(loc["type"] for loc in get_all_locations()))


def get_stats() -> dict:
    """Return summary statistics for the dataset."""
    all_locs = get_all_locations()
    return {
        "total_locations": len(all_locs),
        "total_districts": len(get_districts()),
        "total_population": sum(loc["population"] for loc in all_locs),
        "cities": sum(1 for loc in all_locs if loc["type"] == "city"),
        "towns": sum(1 for loc in all_locs if loc["type"] == "town"),
        "villages": sum(1 for loc in all_locs if loc["type"] == "village"),
    }
