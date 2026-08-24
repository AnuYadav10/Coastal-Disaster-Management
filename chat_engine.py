"""
Gujarat SmartGuide AI — Chat Engine
======================================
Rules-based AI assistant that answers questions about Gujarat locations
using the local dataset. No external LLM required for basic functionality.

The engine uses intent detection + keyword matching to route queries
to the appropriate data service function and format a response.

For OpenAI/LangChain integration (optional advanced mode),
see the `ask_with_llm()` function at the bottom of this file.
"""

import re
from typing import Optional
from data.data_service import (
    get_all_locations,
    get_by_name,
    search_locations,
    get_by_district,
    get_top_by_population,
    get_districts,
    get_stats,
)
from data.weather_service import get_weather_for_location, describe_weather


# ─────────────────────────────────────────────
# Intent Patterns
# ─────────────────────────────────────────────

WEATHER_PATTERNS = [
    r"\bweather\b", r"\btemperature\b", r"\btemp\b", r"\brain\b",
    r"\bhumidity\b", r"\bwind\b", r"\bforecast\b", r"\bclimat\b",
    r"\bhot\b", r"\bcold\b", r"\bsunny\b", r"\brainy\b", r"\bcloudy\b",
]

POPULATION_PATTERNS = [
    r"\bpopulation\b", r"\bpopulat\b", r"\bhow many people\b",
    r"\bhow large\b", r"\bsize\b", r"\bbiggest\b", r"\blargest\b",
    r"\bsmallest\b", r"\bhighest population\b", r"\bmost people\b",
]

DISTRICT_PATTERNS = [
    r"\bdistrict\b", r"\bwhich district\b", r"\bbelongs to\b",
    r"\bpart of\b", r"\bregion\b", r"\barea\b",
]

LIST_PATTERNS = [
    r"\blist\b", r"\bshow me\b", r"\bgive me\b", r"\ball\b",
    r"\bvillages in\b", r"\bcities in\b", r"\blocations in\b",
    r"\bshow locations\b", r"\bshow villages\b",
]

INFO_PATTERNS = [
    r"\btell me about\b", r"\binfo\b", r"\binformation\b",
    r"\bwhat is\b", r"\bwhat about\b", r"\bdescribe\b",
    r"\babout\b", r"\bfamous for\b", r"\bknown for\b",
]

GREETING_PATTERNS = [
    r"^(hi|hello|hey|namaste|namaskar|good morning|good evening|good afternoon|howdy)[\s!.,]*$"
]

HELP_PATTERNS = [
    r"\bhelp\b", r"\bwhat can you\b", r"\bwhat do you\b", r"\bguide\b",
]


def _matches(text: str, patterns: list[str]) -> bool:
    t = text.lower()
    return any(re.search(p, t) for p in patterns)


def _extract_location_name(text: str) -> Optional[str]:
    """
    Try to find a Gujarat location name mentioned in the user query.
    First checks for exact/partial dataset matches, then falls back to
    preposition-based extraction.
    """
    t = text.strip()

    # Direct dataset scan — longest name match wins
    all_locs = get_all_locations()
    all_locs_sorted = sorted(all_locs, key=lambda x: len(x["name"]), reverse=True)
    for loc in all_locs_sorted:
        if loc["name"].lower() in t.lower():
            return loc["name"]

    # Preposition extraction: "in X", "of X", "about X", "for X"
    for prep in ["weather in", "weather of", "about", "tell me about",
                 "info about", "information about", "in", "of", "for", "at"]:
        pattern = rf"\b{re.escape(prep)}\s+([A-Za-z\s]+?)(?:\s*[?.!,]|$)"
        match = re.search(pattern, t, re.IGNORECASE)
        if match:
            candidate = match.group(1).strip()
            if len(candidate) > 1:
                return candidate

    return None


def _extract_district_name(text: str) -> Optional[str]:
    """Extract a district name from the query."""
    districts = get_districts()
    t = text.lower()
    for d in districts:
        if d.lower() in t:
            return d
    return None


# ─────────────────────────────────────────────
# Response Builders
# ─────────────────────────────────────────────

def _weather_response(loc_name: str) -> str:
    weather = get_weather_for_location(loc_name)
    if weather:
        return (
            f"{weather['icon']}  **Weather in {weather['location_name']}**\n\n"
            + describe_weather(weather)
        )
    return f"I don't have weather data for **{loc_name}** in my demo dataset. Try searching for a Gujarat city or village listed in the location database."


def _location_info_response(loc: dict) -> str:
    kf = "\n".join(f"  • {f}" for f in loc.get("key_facts", []))
    return (
        f"📍 **{loc['name']}** — {loc['type'].title()}\n\n"
        f"**District:** {loc['district']}\n"
        f"**Population:** {loc['population']:,}\n"
        f"**Taluka:** {loc.get('taluka', 'N/A')}\n"
        f"**Area:** {loc.get('area_sq_km', 'N/A')} km²\n"
        f"**Nearby City:** {loc.get('nearby_city', 'N/A')}\n\n"
        f"**About:** {loc['description']}\n\n"
        f"**Key Facts:**\n{kf}"
    )


def _list_district_response(district: str) -> str:
    locs = get_by_district(district)
    if not locs:
        return f"I couldn't find any locations in the **{district}** district in my dataset."
    lines = "\n".join(
        f"  • **{l['name']}** ({l['type']}) — Pop: {l['population']:,}" for l in locs
    )
    return (
        f"📋 **Locations in {district} District** ({len(locs)} found)\n\n{lines}\n\n"
        f"*Ask me about any of these for detailed information or weather.*"
    )


def _population_top_response() -> str:
    top = get_top_by_population(5)
    lines = "\n".join(
        f"  {i+1}. **{l['name']}** ({l['district']}) — {l['population']:,}" for i, l in enumerate(top)
    )
    return f"🏙️ **Top 5 Gujarat Locations by Population (Demo Data)**\n\n{lines}"


def _stats_response() -> str:
    s = get_stats()
    return (
        f"📊 **Gujarat SmartGuide Dataset Overview**\n\n"
        f"• **Total locations in dataset:** {s['total_locations']}\n"
        f"• **Districts covered:** {s['total_districts']}\n"
        f"• **Combined population (demo data):** {s['total_population']:,}\n"
        f"• **Cities:** {s['cities']}  |  **Towns:** {s['towns']}  |  **Villages:** {s['villages']}\n\n"
        f"*All figures are from demo/mock data for educational purposes.*"
    )


def _greeting_response() -> str:
    return (
        "🙏 **Kem Cho! Welcome to Gujarat SmartGuide AI!**\n\n"
        "I can help you with:\n"
        "• 🌤️ Weather information for Gujarat locations\n"
        "• 📍 Village and city details\n"
        "• 👥 Population statistics\n"
        "• 🗺️ District information\n"
        "• 📋 Lists of locations by district\n\n"
        "Try asking:\n"
        "> *\"What's the weather in Vapi?\"*\n"
        "> *\"Tell me about Surat.\"*\n"
        "> *\"Show villages in Valsad district.\"*\n"
        "> *\"Which city has the highest population?\"*"
    )


def _help_response() -> str:
    districts = ", ".join(get_districts())
    return (
        "🤖 **How to use Gujarat SmartGuide AI**\n\n"
        "**Weather queries:**\n"
        "  → *\"What is the weather in Bharuch?\"*\n"
        "  → *\"Weather forecast for Surat\"*\n\n"
        "**Location information:**\n"
        "  → *\"Tell me about Ahmedabad\"*\n"
        "  → *\"What is Vadodara known for?\"*\n\n"
        "**Population queries:**\n"
        "  → *\"Which city has the highest population?\"*\n"
        "  → *\"Top 5 cities by population\"*\n\n"
        "**District queries:**\n"
        "  → *\"Show locations in Valsad\"*\n"
        "  → *\"Which district does Vapi belong to?\"*\n\n"
        f"**Available districts:** {districts}\n\n"
        "⚠️ *All data is demo/mock data for educational purposes.*"
    )


def _not_found_response(query: str) -> str:
    results = search_locations(query)
    if results:
        suggestions = ", ".join(f"**{r['name']}**" for r in results[:3])
        return (
            f"I couldn't find an exact match for **\"{query}\"**, but here are some close results: {suggestions}.\n\n"
            f"Try asking more specifically, e.g., *\"Tell me about {results[0]['name']}\"*"
        )
    return (
        f"I don't have information about **\"{query}\"** in my dataset. "
        f"My dataset currently covers {len(get_all_locations())} locations across Gujarat. "
        f"Try searching for cities like Surat, Ahmedabad, Vadodara, Rajkot, or smaller towns like Vapi, Navsari, Bardoli."
    )


# ─────────────────────────────────────────────
# Main Chat Function
# ─────────────────────────────────────────────

def chat(user_message: str) -> str:
    """
    Process a user message and return an AI assistant response.
    Uses rule-based intent detection with local dataset lookups.
    No external API required.
    """
    text = user_message.strip()
    if not text:
        return "Please type a question or location name to get started."

    # ── Greeting
    if _matches(text, GREETING_PATTERNS):
        return _greeting_response()

    # ── Help
    if _matches(text, HELP_PATTERNS):
        return _help_response()

    # ── Stats overview
    if re.search(r"\b(stats|statistics|overview|dataset|how many locations|total)\b", text, re.I):
        return _stats_response()

    # ── Top population query
    if re.search(r"\b(top|highest|most|largest)\b.*\bpopulat\b|\bpopulat.*\b(top|highest|most|largest)\b", text, re.I):
        return _population_top_response()

    # ── District listing
    district = _extract_district_name(text)
    if district and _matches(text, LIST_PATTERNS + DISTRICT_PATTERNS):
        return _list_district_response(district)

    # ── Location-specific queries
    loc_name = _extract_location_name(text)

    if loc_name:
        loc = get_by_name(loc_name)

        # Weather request for a known location
        if _matches(text, WEATHER_PATTERNS):
            if loc:
                return _weather_response(loc["name"])
            return _weather_response(loc_name)

        # District query
        if _matches(text, DISTRICT_PATTERNS) and loc:
            return (
                f"📍 **{loc['name']}** belongs to **{loc['district']} District**.\n\n"
                f"Taluka: {loc.get('taluka', 'N/A')} | Type: {loc['type'].title()} | Population: {loc['population']:,}"
            )

        # General info
        if loc:
            if _matches(text, WEATHER_PATTERNS):
                return _weather_response(loc["name"])
            return _location_info_response(loc)

        # Not found but location was extracted
        return _not_found_response(loc_name)

    # ── Fallback: try district listing
    if district:
        return _list_district_response(district)

    # ── Fallback: try full text search
    results = search_locations(text)
    if results:
        if len(results) == 1:
            loc = results[0]
            if _matches(text, WEATHER_PATTERNS):
                return _weather_response(loc["name"])
            return _location_info_response(loc)
        lines = "\n".join(f"  • **{r['name']}** ({r['district']}) — {r['type'].title()}" for r in results[:5])
        return (
            f"🔍 I found {len(results)} matching location(s):\n\n{lines}\n\n"
            f"*Ask about a specific location for more details, e.g., \"Tell me about {results[0]['name']}\"*"
        )

    # ── Final fallback
    return (
        "I'm sorry, I couldn't understand that query. Try asking about a specific Gujarat location, "
        "for example:\n\n"
        "> *\"What is the weather in Surat?\"*\n"
        "> *\"Tell me about Vapi\"*\n"
        "> *\"Show locations in Bharuch district\"*\n\n"
        "Type **help** for more examples."
    )
