"""
CoastGuard AI — Coastal Disaster Response Agent
=================================================
Central AI agent that handles all cyclone disaster management functions:

  Tool 1 – Cyclone Risk Analysis
  Tool 2 – Fishermen Safety Alert
  Tool 3 – Evacuation Planning
  Tool 4 – Relief Resource Coordination
  Tool 5 – Post-Disaster Damage Assessment

The agent detects user intent and routes to the appropriate tool.
All responses are clearly labelled DEMO/SIMULATED where applicable.

⚠️  This is a HACKATHON PROTOTYPE using IBM Granite-style AI logic.
    It does NOT use real-time data. Do not use for actual emergency decisions.
"""

from __future__ import annotations
import re
from data.disaster_data import (
    get_cyclone_data,
    get_coastal_districts,
    get_district_by_name,
    get_high_risk_districts,
    get_evacuation_data,
    get_priority_evacuations,
    get_relief_resources,
    get_resource_shortages,
    get_damage_reports,
    get_damage_by_severity,
    get_active_alerts,
    get_summary_stats,
)

# ─────────────────────────────────────────────────────────────────────────────
# Risk Scoring
# ─────────────────────────────────────────────────────────────────────────────

RISK_COLOR = {
    "Critical": "🔴",
    "High": "🟠",
    "Moderate": "🟡",
    "Low": "🟢",
}


def _calculate_risk_score(
    wind_speed: float,
    pressure: float,
    rainfall: float,
    distance: float,
    movement_speed: float,
) -> tuple[int, str]:
    """
    Prototype risk score (0–100) using weighted heuristics.
    NOT scientifically validated — for demonstration only.
    """
    score = 0

    # Wind speed contribution (0–40)
    if wind_speed >= 220:
        score += 40
    elif wind_speed >= 180:
        score += 35
    elif wind_speed >= 140:
        score += 30
    elif wind_speed >= 100:
        score += 18
    elif wind_speed >= 65:
        score += 10
    else:
        score += 3

    # Pressure contribution (0–30) — lower = worse
    if pressure <= 900:
        score += 30
    elif pressure <= 930:
        score += 25
    elif pressure <= 960:
        score += 20
    elif pressure <= 990:
        score += 8
    else:
        score += 2

    # Distance from coast (0–20) — closer = higher risk
    if distance <= 50:
        score += 20
    elif distance <= 150:
        score += 16
    elif distance <= 300:
        score += 11
    elif distance <= 500:
        score += 5
    else:
        score += 1

    # Rainfall (0–7)
    if rainfall >= 200:
        score += 7
    elif rainfall >= 100:
        score += 5
    elif rainfall >= 50:
        score += 3
    else:
        score += 1

    # Movement speed (0–3) — faster = slightly more risk
    if movement_speed >= 25:
        score += 3
    elif movement_speed >= 15:
        score += 2
    else:
        score += 1

    score = min(100, max(0, score))

    # Critical: 65+, High: 40+, Moderate: 20+, Low: <20
    if score >= 65:
        level = "Critical"
    elif score >= 40:
        level = "High"
    elif score >= 20:
        level = "Moderate"
    else:
        level = "Low"

    return score, level


# ─────────────────────────────────────────────────────────────────────────────
# TOOL 1 — Cyclone Risk Analysis
# ─────────────────────────────────────────────────────────────────────────────

def tool_cyclone_risk(params: dict | None = None) -> str:
    """Analyse cyclone severity and generate a structured risk report."""
    cy = get_cyclone_data()
    if params:
        cy.update({k: v for k, v in params.items() if v is not None})

    wind = float(cy.get("wind_speed_kmh", 140))
    pressure = float(cy.get("pressure_hpa", 950))
    rainfall = float(cy.get("rainfall_mm", 85))
    distance = float(cy.get("distance_from_coast_km", 180))
    movement_speed = float(cy.get("movement_speed_kmh", 14))
    direction = cy.get("movement_direction", "Northeast")
    name = cy.get("name", "Demo Cyclone")
    area = cy.get("affected_coastal_area", "Saurashtra – Kutch coastline")

    score, level = _calculate_risk_score(wind, pressure, rainfall, distance, movement_speed)
    icon = RISK_COLOR.get(level, "⚪")

    # Affected districts (those with High/Critical)
    affected = [d["name"] for d in get_coastal_districts() if d["risk_level"] in ("Critical", "High")]
    stats = get_summary_stats()

    reason_parts = []
    if wind >= 120:
        reason_parts.append(f"very high wind speed of {wind} km/h")
    if pressure <= 960:
        reason_parts.append(f"very low atmospheric pressure ({pressure} hPa)")
    if distance <= 200:
        reason_parts.append(f"proximity to coast ({distance} km)")
    if rainfall >= 70:
        reason_parts.append(f"heavy rainfall ({rainfall} mm)")
    reason = "; ".join(reason_parts) if reason_parts else "combined meteorological factors"

    return f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌀 CYCLONE RISK ANALYSIS REPORT
⚠️  DEMO DATA — Not for real emergency use
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Cyclone Name:      {name}
Category:          {cy.get('category', 'Very Severe Cyclonic Storm')}
Location:          {cy.get('lat', 'N/A')}°N, {cy.get('lon', 'N/A')}°E
Affected Area:     {area}

{icon} Risk Level:     **{level}**
📊 Risk Score:     {score}/100

Wind Speed:        {wind} km/h
Pressure:          {pressure} hPa
Rainfall:          {rainfall} mm
Distance to Coast: {distance} km
Movement:          {direction} at {movement_speed} km/h

─────────────────────────────────────
Affected Districts: {', '.join(affected)}
Villages at Risk:   {stats['total_villages_at_risk']}
Population at Risk: {stats['total_pop_at_risk']:,}

─────────────────────────────────────
📋 REASON FOR RISK LEVEL:
The {level.upper()} risk level is assigned due to {reason}.

─────────────────────────────────────
✅ RECOMMENDED IMMEDIATE ACTIONS:
{'🚨 EVACUATE all coastal residents within 10 km of shoreline' if level == 'Critical' else '⚠️ Issue pre-evacuation advisory for vulnerable coastal areas'}
{'🚫 Ban all sea fishing — order all boats back to harbour' if level in ('Critical', 'High') else '⚠️ Issue precautionary fishing advisory'}
{'🏥 Activate emergency medical response teams' if level in ('Critical', 'High') else '📋 Put medical teams on standby'}
{'📡 Activate SDRF and NDRF deployment' if level == 'Critical' else '📡 Alert SDRF teams for readiness'}
🔔 Issue public alerts in Gujarati and English

─────────────────────────────────────
Data Source: {cy.get('data_source', 'SIMULATED DEMO DATA')}
Last Updated: {cy.get('last_updated', 'N/A')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""".strip()


# ─────────────────────────────────────────────────────────────────────────────
# TOOL 2 — Fishermen Safety Alert
# ─────────────────────────────────────────────────────────────────────────────

def tool_fishermen_alert(zone: str | None = None, language: str = "both") -> str:
    """Generate a fishermen safety alert based on current cyclone risk."""
    cy = get_cyclone_data()
    _, level = _calculate_risk_score(
        cy["wind_speed_kmh"], cy["pressure_hpa"], cy.get("rainfall_mm", 85),
        cy["distance_from_coast_km"], cy["movement_speed_kmh"],
    )
    icon = RISK_COLOR.get(level, "⚪")

    # Affected fishing zones
    zones = []
    for d in get_coastal_districts():
        if d["risk_level"] in ("Critical", "High"):
            zones.extend(d["fishing_zones"])

    target_zone = zone if zone else "All Gujarat Fishing Zones"

    if level == "Critical":
        action_en = "DO NOT VENTURE INTO SEA. All boats at sea must return to nearest harbour IMMEDIATELY. Fishing is completely banned."
        action_gu = "સમુદ્રમાં જવું નહીં. સમુદ્રમાં તમામ બોટ તાત્કાળ નજીકના બંદરે પાછી ફરો. માછલી પકડવા પર સંપૂર્ણ પ્રતિબંધ."
    elif level == "High":
        action_en = "All fishermen must return to shore immediately. Do not start new fishing trips. Boats should move to safe harbour."
        action_gu = "તમામ માછીમારો તાત્કાળ કિનારે પાછા ફરો. નવી માછીમારી ટ્રીપ શરૂ ન કરો. બોટ સુરક્ષિત બંદર ખસેડો."
    elif level == "Moderate":
        action_en = "Avoid rough sea areas. Return before sunset. Monitor IMD weather updates. Avoid fishing zones in direct cyclone path."
        action_gu = "ઉગ્ર દરિયાઈ વિસ્તારો ટાળો. સૂર્યાસ્ત પહેલા પાછા ફરો. IMD હવામાન અપડેટ ની દેખરેખ રાખો."
    else:
        action_en = "Exercise normal caution. Monitor weather updates. Be prepared to return if conditions worsen."
        action_gu = "સામાન્ય સાવધાની અપનાવો. હવામાન અપડેટ ની દેખરેખ કરો. સ્થિતિ ખરાબ થાય તો પાછા ફરવા તૈયાર રહો."

    return f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚢 FISHERMEN SAFETY ALERT
⚠️  DEMO DATA — Not an official government alert
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ALERT LEVEL:    {icon} {level.upper()}
LOCATION:       {target_zone}
CYCLONE:        {cy['name']}
WIND SPEED:     {cy['wind_speed_kmh']} km/h
DISTANCE:       {cy['distance_from_coast_km']} km from coast

─────────────────────────────────────
🇬🇧 ENGLISH ALERT:
{action_en}

Affected Fishing Zones:
{chr(10).join(f"  • {z}" for z in zones[:6])}

─────────────────────────────────────
🇮🇳 ગુજરાતી ચેતવણી (GUJARATI):
{action_gu}

─────────────────────────────────────
📋 REASON:
Cyclone {cy['name']} with {cy['wind_speed_kmh']} km/h winds is approaching Gujarat coast.
Sea conditions are extremely dangerous. Risk score is elevated to {level.upper()}.

✅ FISHERMEN MUST:
  • Contact Gujarat Maritime Board helpline: 1093 (DEMO)
  • Move boats to safe anchorage
  • Stay with family in inland shelter
  • Do NOT rely on unofficial weather info

Data Source: SIMULATED DEMO DATA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""".strip()


# ─────────────────────────────────────────────────────────────────────────────
# TOOL 3 — Evacuation Planning
# ─────────────────────────────────────────────────────────────────────────────

def tool_evacuation_plan(district: str | None = None, risk_filter: list[str] | None = None) -> str:
    """Generate an evacuation plan for affected villages."""
    if risk_filter is None:
        risk_filter = ["Critical", "High", "Moderate"]

    evac_list = get_priority_evacuations(risk_filter)

    if district:
        evac_list = [e for e in evac_list if district.lower() in e["district"].lower()]

    if not evac_list:
        return f"No evacuation entries found for the specified criteria. Check district name or risk level filter."

    lines = [
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "🚗 EVACUATION PLANNING REPORT",
        "⚠️  DEMO DATA — Routes are NOT official emergency routes",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
    ]

    for e in evac_list:
        capacity_used = e["shelter_occupancy"]
        capacity_total = e["shelter_capacity"]
        capacity_free = capacity_total - capacity_used
        cap_status = "AVAILABLE" if capacity_free >= e["population"] else ("PARTIAL" if capacity_free > 0 else "FULL")
        icon = RISK_COLOR.get(e["risk_level"], "⚪")

        lines.append(f"PRIORITY #{e['priority']}  {icon} {e['risk_level'].upper()}")
        lines.append(f"─────────────────────────────────────")
        lines.append(f"VILLAGE:          {e['village']}")
        lines.append(f"DISTRICT:         {e['district']}")
        lines.append(f"PEOPLE TO MOVE:   {e['population']:,}")
        lines.append(f"SHELTER:          {e['shelter']}")
        lines.append(f"SHELTER CAPACITY: {capacity_total} (Free: {capacity_free})")
        lines.append(f"CAPACITY STATUS:  {cap_status}")
        lines.append(f"ROUTE:            {e['route']}")
        lines.append(f"ROAD STATUS:      {e['road_status']}")
        lines.append(f"DISTANCE:         {e['distance_km']} km")
        lines.append(f"⚠️  WARNING:        {e['warnings']}")
        lines.append("")

    lines.append("─────────────────────────────────────")
    total_people = sum(e["population"] for e in evac_list)
    lines.append(f"TOTAL PEOPLE REQUIRING EVACUATION: {total_people:,}")
    lines.append(f"TOTAL VILLAGES IN PLAN: {len(evac_list)}")
    lines.append("")
    lines.append("📋 NOTE: Critical-risk locations are prioritized first.")
    lines.append("Data Source: SIMULATED DEMO DATA")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# TOOL 4 — Relief Resource Coordination
# ─────────────────────────────────────────────────────────────────────────────

def tool_relief_coordination(district: str | None = None, resource_type: str | None = None) -> str:
    """Analyse relief resources and highlight shortages."""
    resources = get_relief_resources()

    if district:
        resources = [r for r in resources if district.lower() in r["district"].lower()]

    if not resources:
        return f"No relief resource data found for the specified district."

    lines = [
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "🏥 RELIEF RESOURCE COORDINATION REPORT",
        "⚠️  DEMO DATA — Not actual government resource inventory",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
    ]

    resource_labels = {
        "food_packets": "Food Packets",
        "drinking_water_liters": "Drinking Water (L)",
        "medicines_kits": "Medicine Kits",
        "rescue_teams": "Rescue Teams",
        "rescue_boats": "Rescue Boats",
        "emergency_shelters": "Emergency Shelters",
        "medical_teams": "Medical Teams",
    }

    for entry in resources:
        icon = RISK_COLOR.get(entry["risk_level"], "⚪")
        lines.append(f"{icon} {entry['location'].upper()}")
        lines.append(f"District: {entry['district']}  |  Risk Level: {entry['risk_level']}")
        lines.append(f"Population Affected: {entry['population_affected']:,}")
        lines.append(f"─────────────────────────────────────")
        lines.append(f"{'RESOURCE':<28} {'AVAILABLE':>10} {'REQUIRED':>10} {'SHORTAGE':>10} {'STATUS':>10}")
        lines.append(f"{'─'*28} {'─'*10} {'─'*10} {'─'*10} {'─'*10}")

        has_shortage = False
        for res_key, label in resource_labels.items():
            if resource_type and resource_type.lower() not in res_key.lower() and resource_type.lower() not in label.lower():
                continue
            qty = entry["resources"][res_key]
            avail = qty["available"]
            req = qty["required"]
            shortage = max(0, req - avail)
            status = "✅ OK" if shortage == 0 else ("🚨 CRITICAL" if shortage > req * 0.5 else "⚠️  SHORT")
            if shortage > 0:
                has_shortage = True
            lines.append(f"{label:<28} {avail:>10,} {req:>10,} {shortage:>10,} {status:>10}")

        lines.append("")
        if has_shortage:
            lines.append(f"⚠️  PRIORITY: {entry['risk_level'].upper()} — Immediate resource deployment required")
        lines.append("")

    lines.append("─────────────────────────────────────")
    lines.append("📋 RECOMMENDED ACTIONS:")
    lines.append("  • Prioritise Critical and High-risk areas for resource deployment")
    lines.append("  • Request additional SDRF supply convoy from state HQ")
    lines.append("  • Coordinate with NGOs for additional food and water supply")
    lines.append("  • Pre-position medical teams at district hospitals")
    lines.append("")
    lines.append("Data Source: SIMULATED DEMO DATA")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# TOOL 5 — Post-Disaster Damage Assessment
# ─────────────────────────────────────────────────────────────────────────────

def tool_damage_assessment(severity_filter: str | None = None, district: str | None = None) -> str:
    """Generate a structured post-disaster damage assessment report."""
    if severity_filter:
        reports = get_damage_by_severity(severity_filter)
    else:
        reports = get_damage_reports()

    if district:
        reports = [r for r in reports if district.lower() in r["district"].lower()]

    if not reports:
        return "No damage reports found for the specified criteria."

    sev_icon = {"Critical": "🔴", "Severe": "🟠", "Moderate": "🟡", "Minor": "🟢"}
    lines = [
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "🏚️  POST-DISASTER DAMAGE ASSESSMENT",
        "⚠️  AI-ESTIMATED — Not an official government assessment",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
    ]

    total_affected = 0
    for r in sorted(reports, key=lambda x: x["priority"]):
        icon = sev_icon.get(r["severity"], "⚪")
        total_affected += r["affected_people"]
        lines.append(f"REPORT ID:        {r['id']}")
        lines.append(f"LOCATION:         {r['location']}")
        lines.append(f"DAMAGE TYPE:      {r['damage_type']}")
        lines.append(f"SEVERITY:         {icon} {r['severity'].upper()}")
        lines.append(f"AFFECTED PEOPLE:  {r['affected_people']:,}")
        lines.append(f"DESCRIPTION:      {r['description']}")
        lines.append(f"INFRASTRUCTURE:   {', '.join(r['infrastructure_affected'])}")
        lines.append(f"RESPONSE NEEDED:  {r['response_required']}")
        lines.append(f"PRIORITY:         #{r['priority']}")
        lines.append(f"REPORTED:         {r['reported_time']}")
        lines.append(f"SOURCE:           {r['source']}")
        lines.append("")

    lines.append("─────────────────────────────────────")
    lines.append(f"TOTAL DAMAGE REPORTS:  {len(reports)}")
    lines.append(f"TOTAL AFFECTED PEOPLE: {total_affected:,}")
    lines.append("")
    lines.append("⚠️  DISCLAIMER: AI-generated estimates are based on reported/simulated data.")
    lines.append("These are NOT official government damage assessments.")
    lines.append("Data Source: SIMULATED DEMO DATA + USER REPORTED")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# Intent Detection
# ─────────────────────────────────────────────────────────────────────────────

CYCLONE_PATTERNS = [
    r"\bcyclone\b", r"\bstorm\b", r"\bwind\b", r"\bweather\b",
    r"\brisk\b", r"\bhazard\b", r"\bdanger\b", r"\banalysis\b",
    r"\btrack\b", r"\bforecast\b", r"\bpressure\b", r"\bvayu\b",
]
FISHERMEN_PATTERNS = [
    r"\bfish(ermen|er|ing)?\b", r"\bboat\b", r"\bsea\b", r"\bocean\b",
    r"\bcoast\b", r"\bharbou?r\b", r"\bmaarin\b", r"\bmaachhi\b",
    r"\bsailor\b", r"\btrawler\b", r"\bzone\b",
]
EVACUATION_PATTERNS = [
    r"\bevacuat", r"\bshelters?\b", r"\bescape\b", r"\bflee\b",
    r"\bmove\b", r"\bvillages?\b", r"\bpeople\b", r"\brelocate\b",
    r"\bcamp\b", r"\broute\b", r"\bpath\b", r"\bkapacity\b",
    r"\bexodus\b", r"\bwhere.*safe\b", r"\bsafe.*place\b",
    r"\bfirst.*evacuate\b",
    r"\bcapacity\b", r"\bwhich.*village\b", r"\bwhich.*shelter\b",
]
RELIEF_PATTERNS = [
    r"\brelief\b", r"\bresource\b", r"\bfood\b", r"\bwater\b",
    r"\bmedicine\b", r"\bdrug\b", r"\brescue\b", r"\bteam\b",
    r"\bshortage\b", r"\bsupply\b", r"\bstock\b", r"\bration\b",
    r"\baid\b", r"\bhelp\b", r"\bdrinking\b",
]
DAMAGE_PATTERNS = [
    r"\bdamage", r"\bdestroy\b", r"\bcollapse\b", r"\bhouses?\b",
    r"\bbridges?\b", r"\broads?\b", r"\belectric\b", r"\bpower\b",
    r"\bfarm\b", r"\bcrop\b", r"\bassessment\b", r"\breport\b",
    r"\binjury\b", r"\bdeath\b", r"\bflooding\b",
    r"\binfrastructure\b", r"\bdestruct\b", r"\bruined\b",
]
ALERT_PATTERNS = [
    r"\balert\b", r"\bwarning\b", r"\bwarn\b", r"\bnotice\b",
    r"\bgujarati\b", r"\bnews\b", r"\blatest\b",
]
GREETING_PATTERNS = [
    r"^(hi|hello|hey|namaste|namaskar|kem cho|good\s+\w+|howdy)[\s!.,]*$"
]
HELP_PATTERNS = [r"\bhelp\b", r"\bwhat can\b", r"\bwhat do\b", r"\bguide\b"]


def _matches(text: str, patterns: list[str]) -> bool:
    t = text.lower()
    return any(re.search(p, t, re.IGNORECASE) for p in patterns)


def _extract_district(text: str) -> str | None:
    from data.disaster_data import COASTAL_DISTRICTS
    t = text.lower()
    for d in COASTAL_DISTRICTS:
        if d["name"].lower() in t:
            return d["name"]
    return None


def _extract_severity(text: str) -> str | None:
    for sev in ["critical", "severe", "moderate", "minor"]:
        if sev in text.lower():
            return sev.capitalize()
    return None


def _greeting_response() -> str:
    return """🌊 **Kem Cho! Welcome to CoastGuard AI!**

I am the **Coastal Disaster Response Agent** — your central AI system for cyclone and coastal disaster management in Gujarat.

I can help you with:
🌀 **Cyclone Risk Analysis** — Severity, risk score, affected areas
🚢 **Fishermen Safety Alerts** — English & Gujarati warnings
🚗 **Evacuation Planning** — Which villages to evacuate and where
🏥 **Relief Coordination** — Food, water, medicine, rescue teams
🏚️ **Damage Assessment** — Post-cyclone damage reports

**Try asking:**
→ "Analyse cyclone risk for Gujarat"
→ "Give fishermen safety alert"
→ "Which villages need to evacuate?"
→ "Show relief resource shortages"
→ "Show damage reports for Kutch"
→ "Show me active alerts"

⚠️ **DEMO DATA** — All information is simulated for this prototype."""


def _help_response() -> str:
    return """🤖 **CoastGuard AI — Help Guide**

**1. Cyclone Risk Analysis**
→ "Analyse cyclone risk"
→ "What is the current cyclone risk?"
→ "Is Jamnagar at high risk?"

**2. Fishermen Safety Alert**
→ "Give fishermen alert"
→ "Show sea safety warning"
→ "Boat warning in Gujarati"

**3. Evacuation Planning**
→ "Which villages should evacuate?"
→ "Show evacuation plan for Kutch"
→ "Which shelters have capacity?"

**4. Relief Resources**
→ "Show relief shortages"
→ "Water shortage in Kutch?"
→ "Food and medicine availability"

**5. Damage Assessment**
→ "Show severe damage reports"
→ "Damage in Dwarka district"
→ "All damage reports"

**Other commands:**
→ "Show active alerts"
→ "Dashboard overview"
→ "Summary statistics"

⚠️ All data is **DEMO/SIMULATED** — Not for real emergency use."""


def _district_risk_response(district_name: str) -> str:
    d = get_district_by_name(district_name)
    if not d:
        return f"I don't have risk data for '{district_name}'. Available coastal districts: " + \
               ", ".join(x["name"] for x in get_coastal_districts())
    icon = RISK_COLOR.get(d["risk_level"], "⚪")
    zones = ", ".join(d["fishing_zones"])
    return f"""
{icon} **Risk Assessment — {d['name']} District**

Risk Level:         **{d['risk_level']}**
Population at Risk: {d['pop_at_risk']:,}
Villages at Risk:   {d['villages_at_risk']}
Coastal Length:     {d['coastal_length_km']} km
Fishing Zones:      {zones}

{'⚠️ IMMEDIATE ACTION REQUIRED — Evacuate low-lying coastal areas NOW' if d['risk_level'] == 'Critical' else '⚠️ High alert — monitor situation and prepare for possible evacuation' if d['risk_level'] == 'High' else '📋 Moderate risk — issue precautionary advisories'}

Data Source: SIMULATED DEMO DATA
""".strip()


def _alerts_response() -> str:
    alerts = get_active_alerts()
    level_icon = {"RED": "🔴", "ORANGE": "🟠", "YELLOW": "🟡"}
    lines = [
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "🔔 ACTIVE ALERTS",
        "⚠️  DEMO DATA — Not official government alerts",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
    ]
    for a in alerts:
        li = level_icon.get(a["level"], "⚪")
        lines.append(f"{li} [{a['level']}] {a['type']}")
        lines.append(f"Area: {a['area']}")
        lines.append(f"🇬🇧 {a['message_en']}")
        lines.append(f"🇮🇳 {a['message_gu']}")
        lines.append(f"Issued: {a['issued_time']} by {a['authority']}")
        lines.append("")
    return "\n".join(lines)


def _overview_response() -> str:
    stats = get_summary_stats()
    cy = get_cyclone_data()
    return f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌊 COASTGUARD AI — SITUATION OVERVIEW
⚠️  DEMO DATA — Simulated Scenario
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌀 CYCLONE: {stats['cyclone_name']}
   Wind Speed:   {stats['cyclone_wind_speed']} km/h
   Risk Level:   🔴 CRITICAL

🗺️  AFFECTED COASTAL DISTRICTS
   Critical:     {stats['critical_districts']} districts
   High Risk:    {stats['high_districts']} districts
   Villages:     {stats['total_villages_at_risk']}
   Population:   {stats['total_pop_at_risk']:,} at risk

🔔 ACTIVE ALERTS:        {stats['active_alerts']}
🚗 EVACUATION SITES:     {stats['evacuation_villages']}
🏚️  DAMAGE REPORTS:      {stats['damage_reports']}

Critical Districts: Kutch, Jamnagar, Devbhumi Dwarka

Type "cyclone risk", "fishermen alert", "evacuation plan",
"relief resources", or "damage reports" for detailed info.

Data Source: SIMULATED DEMO DATA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""".strip()


# ─────────────────────────────────────────────────────────────────────────────
# Main Agent Entry Point
# ─────────────────────────────────────────────────────────────────────────────

def coastal_agent(user_message: str) -> str:
    """
    Central Coastal Disaster Response Agent.
    Detects user intent and routes to the correct tool.
    """
    text = user_message.strip()
    if not text:
        return "Please type a question or command to get started."

    # Greeting
    if _matches(text, GREETING_PATTERNS):
        return _greeting_response()

    # Help
    if _matches(text, HELP_PATTERNS):
        return _help_response()

    # Overview / summary
    if re.search(r"\b(overview|summary|status|situation|dashboard)\b", text, re.I):
        return _overview_response()

    # Active alerts
    if _matches(text, ALERT_PATTERNS) and not _matches(text, FISHERMEN_PATTERNS + CYCLONE_PATTERNS + EVACUATION_PATTERNS):
        return _alerts_response()

    # District-specific risk check
    district = _extract_district(text)
    if district and re.search(r"\b(risk|danger|safe|affect|status|situation)\b", text, re.I):
        return _district_risk_response(district)

    # TOOL 2: Fishermen safety alert — check before cyclone (overlapping keywords)
    if _matches(text, FISHERMEN_PATTERNS):
        return tool_fishermen_alert(district)

    # TOOL 1: Cyclone risk analysis
    if _matches(text, CYCLONE_PATTERNS):
        return tool_cyclone_risk()

    # TOOL 3: Evacuation planning
    if _matches(text, EVACUATION_PATTERNS):
        rf = None
        if re.search(r"\bcritical\b", text, re.I):
            rf = ["Critical"]
        elif re.search(r"\bhigh\b", text, re.I):
            rf = ["Critical", "High"]
        return tool_evacuation_plan(district, rf)

    # TOOL 4: Relief resources
    if _matches(text, RELIEF_PATTERNS):
        res_type = None
        for rt in ["food", "water", "medicine", "rescue", "boat", "shelter", "medical"]:
            if rt in text.lower():
                res_type = rt
                break
        return tool_relief_coordination(district, res_type)

    # TOOL 5: Damage assessment
    if _matches(text, DAMAGE_PATTERNS):
        severity = _extract_severity(text)
        return tool_damage_assessment(severity, district)

    # Alert as fallback for "alert" + any context
    if _matches(text, ALERT_PATTERNS):
        return _alerts_response()

    # General district query
    if district:
        return _district_risk_response(district)

    # Final fallback
    return f"""I understand you're asking about: "{text}"

I couldn't determine which disaster management tool to use. Here's what I can help with:

🌀 **Cyclone risk** — Try: "Analyse cyclone risk for Gujarat"
🚢 **Fishermen alert** — Try: "Give fishermen safety warning"
🚗 **Evacuation** — Try: "Which villages need to evacuate?"
🏥 **Relief resources** — Try: "Show water shortage in Kutch"
🏚️ **Damage reports** — Try: "Show severe damage reports"
🔔 **Active alerts** — Try: "Show active alerts"

Type **help** for the full guide or **overview** for a situation summary.
⚠️ All data is SIMULATED DEMO DATA."""
