"""
CoastGuard AI — Disaster Data Service
=======================================
Provides SIMULATED / DEMO data for the CoastGuard AI prototype.

⚠️  ALL DATA IS DEMO/SIMULATED — Not for real emergency decision-making.
     Do not use for actual cyclone response or evacuation planning.

When real APIs are available, replace the `get_*` functions with live calls
to IMD (India Meteorological Department), NDMA, or Gujarat SDMA feeds.
"""

from __future__ import annotations

# ─────────────────────────────────────────────────────────────────────────────
# Demo Cyclone Scenario
# ─────────────────────────────────────────────────────────────────────────────

DEMO_CYCLONE: dict = {
    "name": "Demo Cyclone VAYU",
    "category": "Very Severe Cyclonic Storm",
    "lat": 21.8,
    "lon": 68.4,
    "wind_speed_kmh": 140,
    "pressure_hpa": 950,
    "rainfall_mm": 85,
    "movement_direction": "Northeast",
    "movement_speed_kmh": 14,
    "distance_from_coast_km": 180,
    "affected_coastal_area": "Saurashtra – Kutch coastline",
    "data_source": "SIMULATED DEMO DATA",
    "last_updated": "2024-06-12 09:00 IST",
}

# ─────────────────────────────────────────────────────────────────────────────
# Gujarat Coastal Districts
# ─────────────────────────────────────────────────────────────────────────────

COASTAL_DISTRICTS: list[dict] = [
    {
        "name": "Kutch",
        "population": 2092371,
        "coastal_length_km": 400,
        "fishing_zones": ["Gulf of Kutch Zone A", "Gulf of Kutch Zone B"],
        "lat": 23.73,
        "lon": 69.86,
        "risk_level": "Critical",
        "villages_at_risk": 42,
        "pop_at_risk": 180000,
        "color": "#dc2626",
    },
    {
        "name": "Jamnagar",
        "population": 2160119,
        "coastal_length_km": 337,
        "fishing_zones": ["Jamnagar Coastal Zone", "Marine National Park Zone"],
        "lat": 22.47,
        "lon": 70.06,
        "risk_level": "Critical",
        "villages_at_risk": 38,
        "pop_at_risk": 165000,
        "color": "#dc2626",
    },
    {
        "name": "Devbhumi Dwarka",
        "population": 752484,
        "coastal_length_km": 190,
        "fishing_zones": ["Dwarka Fishing Zone", "Okha Zone"],
        "lat": 22.24,
        "lon": 68.96,
        "risk_level": "Critical",
        "villages_at_risk": 29,
        "pop_at_risk": 95000,
        "color": "#dc2626",
    },
    {
        "name": "Porbandar",
        "population": 586062,
        "coastal_length_km": 100,
        "fishing_zones": ["Porbandar Deep Sea Zone", "Chara Zone"],
        "lat": 21.64,
        "lon": 69.61,
        "risk_level": "High",
        "villages_at_risk": 22,
        "pop_at_risk": 72000,
        "color": "#f97316",
    },
    {
        "name": "Junagadh",
        "population": 2743082,
        "coastal_length_km": 58,
        "fishing_zones": ["Veraval Zone"],
        "lat": 21.52,
        "lon": 70.45,
        "risk_level": "High",
        "villages_at_risk": 18,
        "pop_at_risk": 58000,
        "color": "#f97316",
    },
    {
        "name": "Gir Somnath",
        "population": 1244376,
        "coastal_length_km": 135,
        "fishing_zones": ["Somnath Zone", "Diu Coastal Zone"],
        "lat": 20.91,
        "lon": 70.37,
        "risk_level": "High",
        "villages_at_risk": 24,
        "pop_at_risk": 62000,
        "color": "#f97316",
    },
    {
        "name": "Amreli",
        "population": 1514190,
        "coastal_length_km": 110,
        "fishing_zones": ["Jafrabad Zone"],
        "lat": 21.60,
        "lon": 71.22,
        "risk_level": "Moderate",
        "villages_at_risk": 14,
        "pop_at_risk": 38000,
        "color": "#f59e0b",
    },
    {
        "name": "Bhavnagar",
        "population": 2877961,
        "coastal_length_km": 188,
        "fishing_zones": ["Bhavnagar Gulf Zone", "Alang Zone"],
        "lat": 21.76,
        "lon": 72.15,
        "risk_level": "Moderate",
        "villages_at_risk": 12,
        "pop_at_risk": 42000,
        "color": "#f59e0b",
    },
    {
        "name": "Bharuch",
        "population": 1551026,
        "coastal_length_km": 64,
        "fishing_zones": ["Gulf of Khambhat North"],
        "lat": 21.70,
        "lon": 72.99,
        "risk_level": "Moderate",
        "villages_at_risk": 8,
        "pop_at_risk": 22000,
        "color": "#f59e0b",
    },
    {
        "name": "Surat",
        "population": 6081322,
        "coastal_length_km": 50,
        "fishing_zones": ["Surat Coastal Zone"],
        "lat": 21.17,
        "lon": 72.83,
        "risk_level": "Low",
        "villages_at_risk": 5,
        "pop_at_risk": 15000,
        "color": "#22c55e",
    },
    {
        "name": "Navsari",
        "population": 1330711,
        "coastal_length_km": 40,
        "fishing_zones": ["Dandi Zone"],
        "lat": 20.95,
        "lon": 72.92,
        "risk_level": "Low",
        "villages_at_risk": 4,
        "pop_at_risk": 10000,
        "color": "#22c55e",
    },
    {
        "name": "Valsad",
        "population": 1703068,
        "coastal_length_km": 57,
        "fishing_zones": ["Valsad Coastal Zone"],
        "lat": 20.60,
        "lon": 72.93,
        "risk_level": "Low",
        "villages_at_risk": 3,
        "pop_at_risk": 8000,
        "color": "#22c55e",
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# Evacuation Data
# ─────────────────────────────────────────────────────────────────────────────

EVACUATION_DATA: list[dict] = [
    {
        "village": "Maska",
        "district": "Kutch",
        "population": 4200,
        "risk_level": "Critical",
        "priority": 1,
        "shelter": "Mandvi Government School",
        "shelter_capacity": 800,
        "shelter_occupancy": 120,
        "route": "Maska → NH-341 → Mandvi Town (14 km)",
        "road_status": "Open",
        "distance_km": 14,
        "warnings": "Low-lying area, storm surge expected",
    },
    {
        "village": "Roha",
        "district": "Devbhumi Dwarka",
        "population": 3800,
        "risk_level": "Critical",
        "priority": 2,
        "shelter": "Okha Community Hall",
        "shelter_capacity": 600,
        "shelter_occupancy": 80,
        "route": "Roha → SH-25 → Okha Port Road (18 km)",
        "road_status": "Open",
        "distance_km": 18,
        "warnings": "Coastal flooding zone, evacuate immediately",
    },
    {
        "village": "Narara",
        "district": "Jamnagar",
        "population": 2900,
        "risk_level": "Critical",
        "priority": 3,
        "shelter": "Jamnagar Sports Complex",
        "shelter_capacity": 1200,
        "shelter_occupancy": 300,
        "route": "Narara → NH-27 → Jamnagar City (22 km)",
        "road_status": "Open",
        "distance_km": 22,
        "warnings": "Near Marine National Park, tidal surge risk",
    },
    {
        "village": "Salaya",
        "district": "Devbhumi Dwarka",
        "population": 5600,
        "risk_level": "Critical",
        "priority": 4,
        "shelter": "Jodiya Taluka School Campus",
        "shelter_capacity": 900,
        "shelter_occupancy": 150,
        "route": "Salaya → SH-6 → Jodiya (28 km)",
        "road_status": "Open",
        "distance_km": 28,
        "warnings": "Fishing harbour area, direct cyclone path",
    },
    {
        "village": "Madhavpur",
        "district": "Porbandar",
        "population": 6200,
        "risk_level": "High",
        "priority": 5,
        "shelter": "Porbandar Civil Hospital Campus",
        "shelter_capacity": 1500,
        "shelter_occupancy": 200,
        "route": "Madhavpur → NH-51 → Porbandar City (35 km)",
        "road_status": "Open",
        "distance_km": 35,
        "warnings": "Beach area, strong wave surge expected",
    },
    {
        "village": "Chorwad",
        "district": "Gir Somnath",
        "population": 8400,
        "risk_level": "High",
        "priority": 6,
        "shelter": "Veraval District School",
        "shelter_capacity": 2000,
        "shelter_occupancy": 450,
        "route": "Chorwad → SH-98 → Veraval Town (12 km)",
        "road_status": "Open",
        "distance_km": 12,
        "warnings": "Fishing community area, coordinate with NDRF",
    },
    {
        "village": "Jafrabad",
        "district": "Amreli",
        "population": 11200,
        "risk_level": "Moderate",
        "priority": 7,
        "shelter": "Jafrabad Town School",
        "shelter_capacity": 1800,
        "shelter_occupancy": 300,
        "route": "Coastal Road → NH-151A → Jafrabad Town (8 km)",
        "road_status": "Open",
        "distance_km": 8,
        "warnings": "Monitor water levels, evacuate if surge warning issued",
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# Relief Resources
# ─────────────────────────────────────────────────────────────────────────────

RELIEF_RESOURCES: list[dict] = [
    {
        "location": "Kutch – Bhuj Relief Camp",
        "district": "Kutch",
        "population_affected": 12000,
        "risk_level": "Critical",
        "resources": {
            "food_packets": {"available": 3000, "required": 12000},
            "drinking_water_liters": {"available": 15000, "required": 60000},
            "medicines_kits": {"available": 200, "required": 600},
            "rescue_teams": {"available": 3, "required": 8},
            "rescue_boats": {"available": 4, "required": 12},
            "emergency_shelters": {"available": 200, "required": 600},
            "medical_teams": {"available": 1, "required": 4},
        },
    },
    {
        "location": "Jamnagar – Navsari Relief Point",
        "district": "Jamnagar",
        "population_affected": 9500,
        "risk_level": "Critical",
        "resources": {
            "food_packets": {"available": 4000, "required": 9500},
            "drinking_water_liters": {"available": 20000, "required": 47500},
            "medicines_kits": {"available": 300, "required": 475},
            "rescue_teams": {"available": 4, "required": 7},
            "rescue_boats": {"available": 6, "required": 10},
            "emergency_shelters": {"available": 350, "required": 500},
            "medical_teams": {"available": 2, "required": 4},
        },
    },
    {
        "location": "Dwarka Relief Centre",
        "district": "Devbhumi Dwarka",
        "population_affected": 7200,
        "risk_level": "Critical",
        "resources": {
            "food_packets": {"available": 2500, "required": 7200},
            "drinking_water_liters": {"available": 10000, "required": 36000},
            "medicines_kits": {"available": 150, "required": 360},
            "rescue_teams": {"available": 2, "required": 6},
            "rescue_boats": {"available": 3, "required": 8},
            "emergency_shelters": {"available": 180, "required": 400},
            "medical_teams": {"available": 1, "required": 3},
        },
    },
    {
        "location": "Porbandar Coastal Camp",
        "district": "Porbandar",
        "population_affected": 5800,
        "risk_level": "High",
        "resources": {
            "food_packets": {"available": 3500, "required": 5800},
            "drinking_water_liters": {"available": 18000, "required": 29000},
            "medicines_kits": {"available": 250, "required": 290},
            "rescue_teams": {"available": 3, "required": 5},
            "rescue_boats": {"available": 5, "required": 7},
            "emergency_shelters": {"available": 300, "required": 350},
            "medical_teams": {"available": 2, "required": 3},
        },
    },
    {
        "location": "Veraval – Gir Somnath Base",
        "district": "Gir Somnath",
        "population_affected": 4200,
        "risk_level": "High",
        "resources": {
            "food_packets": {"available": 2800, "required": 4200},
            "drinking_water_liters": {"available": 14000, "required": 21000},
            "medicines_kits": {"available": 200, "required": 210},
            "rescue_teams": {"available": 2, "required": 4},
            "rescue_boats": {"available": 4, "required": 6},
            "emergency_shelters": {"available": 250, "required": 300},
            "medical_teams": {"available": 1, "required": 2},
        },
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# Damage Reports
# ─────────────────────────────────────────────────────────────────────────────

DAMAGE_REPORTS: list[dict] = [
    {
        "id": "DR-001",
        "location": "Maska Village, Kutch",
        "district": "Kutch",
        "damage_type": "Houses",
        "severity": "Severe",
        "affected_people": 1800,
        "description": "Approximately 240 houses severely damaged or collapsed due to cyclone winds and storm surge",
        "infrastructure_affected": ["Residential buildings", "Boundary walls", "Roofing"],
        "response_required": "Immediate NDRF deployment, temporary shelter, relief material",
        "priority": 1,
        "reported_time": "2024-06-12 11:30 IST",
        "source": "USER REPORTED",
    },
    {
        "id": "DR-002",
        "location": "Okha Port, Devbhumi Dwarka",
        "district": "Devbhumi Dwarka",
        "damage_type": "Boats & Fishing Infrastructure",
        "severity": "Critical",
        "affected_people": 2400,
        "description": "Over 180 fishing boats damaged or sunk at Okha harbour. Fishing nets and equipment destroyed.",
        "infrastructure_affected": ["Fishing boats", "Harbour jetty", "Fish market", "Cold storage"],
        "response_required": "Coast Guard rescue, livelihood assessment, compensation survey",
        "priority": 1,
        "reported_time": "2024-06-12 10:45 IST",
        "source": "USER REPORTED",
    },
    {
        "id": "DR-003",
        "location": "NH-341, Kutch District",
        "district": "Kutch",
        "damage_type": "Roads & Bridges",
        "severity": "Moderate",
        "affected_people": 45000,
        "description": "Section of NH-341 flooded and damaged near Mandvi. Bridge over Rukmavati river cracked.",
        "infrastructure_affected": ["National highway", "Road bridge", "Culverts"],
        "response_required": "PWD emergency repair team, alternate route activation",
        "priority": 2,
        "reported_time": "2024-06-12 12:00 IST",
        "source": "AI ESTIMATED",
    },
    {
        "id": "DR-004",
        "location": "Salaya Coastal Village, Dwarka",
        "district": "Devbhumi Dwarka",
        "damage_type": "Electricity Infrastructure",
        "severity": "Severe",
        "affected_people": 8200,
        "description": "High-tension power lines snapped. Multiple transformer stations flooded. 12 villages without electricity.",
        "infrastructure_affected": ["Transmission lines", "Transformer stations", "Distribution network"],
        "response_required": "PGVCL emergency team, generator deployment",
        "priority": 2,
        "reported_time": "2024-06-12 11:00 IST",
        "source": "USER REPORTED",
    },
    {
        "id": "DR-005",
        "location": "Madhavpur Beach Area, Porbandar",
        "district": "Porbandar",
        "damage_type": "Agricultural Land",
        "severity": "Moderate",
        "affected_people": 3600,
        "description": "Estimated 1,200 hectares of groundnut and cotton crops destroyed by saltwater flooding.",
        "infrastructure_affected": ["Agricultural fields", "Irrigation canals", "Farm storage"],
        "response_required": "Crop loss assessment, farmer compensation process",
        "priority": 3,
        "reported_time": "2024-06-12 13:00 IST",
        "source": "AI ESTIMATED",
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# Active Alerts
# ─────────────────────────────────────────────────────────────────────────────

ACTIVE_ALERTS: list[dict] = [
    {
        "id": "AL-001",
        "type": "CYCLONE WARNING",
        "level": "RED",
        "area": "Kutch, Jamnagar, Devbhumi Dwarka",
        "message_en": "SEVERE CYCLONIC STORM WARNING: Cyclone VAYU is 180 km from Gujarat coast. Expected landfall in 24-36 hours near Kutch-Dwarka coast. All coastal residents must evacuate immediately.",
        "message_gu": "ગંભીર ચક્રવાત તોફાન ચેતવણી: ચક્રવાત VAYU ગુજરાત તટ થી 180 કિ.મી. દૂર છે. 24-36 કલાકમાં કચ્છ-દ્વારકા તટ નજીક ઉતરાણ અપેક્ષિત. તમામ દરિયાઈ રહેવાસીઓ તાત્કાલિક સ્થળાંતર કરે.",
        "issued_time": "2024-06-12 09:00 IST",
        "authority": "IMD Ahmedabad (SIMULATED)",
    },
    {
        "id": "AL-002",
        "type": "FISHERMEN SAFETY ALERT",
        "level": "RED",
        "area": "All Gujarat fishing zones",
        "message_en": "DO NOT VENTURE INTO SEA: All fishermen must immediately return to shore. No fishing boats should be in the sea. Port entry being coordinated by Coast Guard.",
        "message_gu": "સમુદ્રમાં ન જાઓ: તમામ માછીમારો તાત્કાલિક કિનારે પાછા આવો. કોઈ માછીમારી બોટ સમુદ્રમાં ન હોવી જોઈએ. ભારતીય દરિયાઈ સુરક્ષા દ્વારા બંદર પ્રવેશ સંકલન કરવામાં આવી રહ્યું છે.",
        "issued_time": "2024-06-12 08:30 IST",
        "authority": "Gujarat Maritime Board (SIMULATED)",
    },
    {
        "id": "AL-003",
        "type": "EVACUATION ORDER",
        "level": "ORANGE",
        "area": "Porbandar, Junagadh coastal villages",
        "message_en": "EVACUATION ADVISORY: Residents of coastal villages within 5 km of shoreline in Porbandar and Junagadh districts should move to designated relief shelters.",
        "message_gu": "સ્થળાંતર સૂચના: પોરબંદર અને જૂનાગઢ જિલ્લામાં દરિયાકિનારાથી 5 કિ.મી. ની અંદરના ગ્રામ નિવાસીઓ નિયત રાહત આશ્રયસ્થળો પર ખસેડવા.",
        "issued_time": "2024-06-12 10:00 IST",
        "authority": "Gujarat Revenue Department (SIMULATED)",
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# Service Functions
# ─────────────────────────────────────────────────────────────────────────────

def get_cyclone_data() -> dict:
    """Return the current demo cyclone scenario data."""
    return DEMO_CYCLONE.copy()


def get_coastal_districts() -> list[dict]:
    """Return all coastal district risk data."""
    return COASTAL_DISTRICTS


def get_district_by_name(name: str) -> dict | None:
    """Return district data by name (case-insensitive partial match)."""
    n = name.strip().lower()
    for d in COASTAL_DISTRICTS:
        if n in d["name"].lower() or d["name"].lower() in n:
            return d
    return None


def get_high_risk_districts() -> list[dict]:
    """Return districts with High or Critical risk levels."""
    return [d for d in COASTAL_DISTRICTS if d["risk_level"] in ("Critical", "High")]


def get_evacuation_data() -> list[dict]:
    """Return all evacuation planning records."""
    return EVACUATION_DATA


def get_priority_evacuations(levels: list[str] | None = None) -> list[dict]:
    """Return evacuations filtered by risk level, sorted by priority."""
    data = EVACUATION_DATA
    if levels:
        data = [v for v in data if v["risk_level"] in levels]
    return sorted(data, key=lambda x: x["priority"])


def get_relief_resources() -> list[dict]:
    """Return all relief resource records."""
    return RELIEF_RESOURCES


def get_resource_shortages() -> list[dict]:
    """Return relief entries where at least one resource is short."""
    shortages = []
    for entry in RELIEF_RESOURCES:
        short_items = []
        for resource, qty in entry["resources"].items():
            if qty["available"] < qty["required"]:
                short_items.append({
                    "resource": resource,
                    "available": qty["available"],
                    "required": qty["required"],
                    "shortage": qty["required"] - qty["available"],
                })
        if short_items:
            shortages.append({**entry, "shortages": short_items})
    return shortages


def get_damage_reports() -> list[dict]:
    """Return all damage reports."""
    return DAMAGE_REPORTS


def get_damage_by_severity(severity: str) -> list[dict]:
    """Return damage reports filtered by severity."""
    return [r for r in DAMAGE_REPORTS if r["severity"].lower() == severity.lower()]


def get_active_alerts() -> list[dict]:
    """Return all active alerts."""
    return ACTIVE_ALERTS


def get_summary_stats() -> dict:
    """Return summary statistics for the dashboard."""
    districts = COASTAL_DISTRICTS
    return {
        "total_districts_at_risk": len([d for d in districts if d["risk_level"] != "Low"]),
        "critical_districts": len([d for d in districts if d["risk_level"] == "Critical"]),
        "high_districts": len([d for d in districts if d["risk_level"] == "High"]),
        "total_pop_at_risk": sum(d["pop_at_risk"] for d in districts),
        "total_villages_at_risk": sum(d["villages_at_risk"] for d in districts),
        "active_alerts": len(ACTIVE_ALERTS),
        "evacuation_villages": len(EVACUATION_DATA),
        "damage_reports": len(DAMAGE_REPORTS),
        "cyclone_wind_speed": DEMO_CYCLONE["wind_speed_kmh"],
        "cyclone_name": DEMO_CYCLONE["name"],
    }
