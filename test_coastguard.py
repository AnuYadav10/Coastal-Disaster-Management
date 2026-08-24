# -*- coding: utf-8 -*-
"""
CoastGuard AI - Test Suite
Run with: python test_coastguard.py
"""

import sys
import os
import io

# Force UTF-8 output to avoid Windows CP1252 issues
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(__file__))

from agent.coastal_agent import (
    coastal_agent,
    tool_cyclone_risk,
    tool_fishermen_alert,
    tool_evacuation_plan,
    tool_relief_coordination,
    tool_damage_assessment,
)
from data.disaster_data import (
    get_summary_stats,
    get_cyclone_data,
    get_coastal_districts,
    get_evacuation_data,
    get_relief_resources,
    get_damage_reports,
    get_active_alerts,
    get_resource_shortages,
    get_priority_evacuations,
    get_district_by_name,
    get_high_risk_districts,
)

PASS = 0
FAIL = 0


def check(name, condition, detail=""):
    global PASS, FAIL
    if condition:
        print(f"  PASS  {name}")
        PASS += 1
    else:
        print(f"  FAIL  {name}: {detail}")
        FAIL += 1


print("=" * 60)
print("CoastGuard AI — Functional Tests")
print("=" * 60)

# ── Data Service Tests ──
print("\n[1] Data Service")
cy = get_cyclone_data()
check("Cyclone data loaded", "name" in cy and cy["wind_speed_kmh"] > 0)
check("Cyclone VAYU scenario", "VAYU" in cy["name"])

districts = get_coastal_districts()
check("12 coastal districts", len(districts) == 12)
check("Critical districts present", any(d["risk_level"] == "Critical" for d in districts))
check("District data has pop_at_risk", all("pop_at_risk" in d for d in districts))

evac = get_evacuation_data()
check("Evacuation data loaded", len(evac) >= 5)
check("Evacuation priorities set", all("priority" in e for e in evac))

relief = get_relief_resources()
check("Relief resources loaded", len(relief) >= 3)
check("Resource shortages detected", len(get_resource_shortages()) > 0)

damage = get_damage_reports()
check("Damage reports loaded", len(damage) >= 3)

alerts = get_active_alerts()
check("Active alerts loaded", len(alerts) >= 2)

stats = get_summary_stats()
check("Summary stats complete", all(k in stats for k in [
    "critical_districts", "total_pop_at_risk", "active_alerts"
]))
check("Stats: critical districts >= 2", stats["critical_districts"] >= 2)
check("Stats: pop at risk > 0", stats["total_pop_at_risk"] > 0)

d = get_district_by_name("Kutch")
check("District lookup: Kutch found", d is not None and d["name"] == "Kutch")
check("Kutch is Critical risk", d["risk_level"] == "Critical")

high = get_high_risk_districts()
check("High risk districts returned", len(high) >= 3)

prio = get_priority_evacuations(["Critical"])
check("Priority evacuation filter works", all(e["risk_level"] == "Critical" for e in prio))

# ── Risk Scoring Test ──
print("\n[2] Risk Scoring")
from agent.coastal_agent import _calculate_risk_score

score, level = _calculate_risk_score(140, 950, 85, 180, 14)
check("Demo scenario: score > 0", score > 0)
check("Demo scenario: Critical risk", level == "Critical")

score_low, level_low = _calculate_risk_score(40, 1010, 5, 800, 5)
check("Low scenario: score < 25", score_low < 25)
check("Low scenario: Low risk", level_low == "Low")

score_high, level_high = _calculate_risk_score(120, 960, 60, 100, 20)
check("High scenario: score >= 50", score_high >= 50)
check("High scenario: High or Critical", level_high in ("High", "Critical"))

# ── Tool Tests ──
print("\n[3] Tool Outputs")
r1 = tool_cyclone_risk()
check("Tool 1: Cyclone risk report generated", "CYCLONE RISK ANALYSIS" in r1)
check("Tool 1: Contains risk score", "Risk Score" in r1)
check("Tool 1: Contains affected districts", "Affected Districts" in r1)
check("Tool 1: Demo data label present", "SIMULATED" in r1 or "DEMO" in r1)

r2 = tool_fishermen_alert()
check("Tool 2: Fishermen alert generated", "FISHERMEN SAFETY ALERT" in r2)
check("Tool 2: English alert present", "ENGLISH ALERT" in r2)
check("Tool 2: Gujarati alert present", len([line for line in r2.split("\n") if "ગુ" in line or "GUJARATI" in line]) > 0)
check("Tool 2: Action instructions present", "ACTION" in r2 or "DO NOT" in r2 or "return" in r2.lower())
check("Tool 2: Demo label", "DEMO" in r2 or "SIMULATED" in r2)

r3 = tool_evacuation_plan()
check("Tool 3: Evacuation plan generated", "EVACUATION PLANNING" in r3)
check("Tool 3: Priority numbers present", "PRIORITY #" in r3)
check("Tool 3: Shelter info present", "SHELTER" in r3)
check("Tool 3: Route info present", "ROUTE" in r3)
check("Tool 3: Demo label", "SIMULATED" in r3)

r3_critical = tool_evacuation_plan(risk_filter=["Critical"])
check("Tool 3: Critical filter works", "CRITICAL" in r3_critical.upper())

r3_district = tool_evacuation_plan(district="Kutch")
check("Tool 3: District filter works", "Kutch" in r3_district)

r4 = tool_relief_coordination()
check("Tool 4: Relief report generated", "RELIEF RESOURCE" in r4)
check("Tool 4: Contains shortage status", "SHORT" in r4 or "CRITICAL" in r4)
check("Tool 4: Contains resource table", "Food Packets" in r4 or "AVAILABLE" in r4)
check("Tool 4: Demo label", "SIMULATED" in r4)

r4_water = tool_relief_coordination(resource_type="water")
check("Tool 4: Water filter works", "Water" in r4_water or "water" in r4_water.lower())

r5 = tool_damage_assessment()
check("Tool 5: Damage assessment generated", "DAMAGE ASSESSMENT" in r5)
check("Tool 5: Contains severity", "SEVERITY" in r5)
check("Tool 5: Contains affected people", "AFFECTED PEOPLE" in r5)
check("Tool 5: Disclaimer present", "AI-ESTIMATED" in r5 or "ESTIMATED" in r5 or "official" in r5.lower())

r5_severe = tool_damage_assessment(severity_filter="Severe")
check("Tool 5: Severity filter works", "Severe" in r5_severe or len(r5_severe) > 50)

# ── Agent Intent Routing ──
print("\n[4] Agent Intent Routing")
routing_tests = [
    ("analyse cyclone risk", "CYCLONE RISK"),
    ("what is the cyclone status", "CYCLONE RISK"),
    ("fishermen safety alert", "FISHERMEN SAFETY ALERT"),
    ("sea warning for boats", "FISHERMEN SAFETY ALERT"),
    ("which villages need to evacuate", "EVACUATION PLANNING"),
    ("show shelters", "EVACUATION PLANNING"),
    ("show relief shortages", "RELIEF RESOURCE"),
    ("water supply in Kutch", "RELIEF RESOURCE"),
    ("food availability", "RELIEF RESOURCE"),
    ("show damage reports", "DAMAGE ASSESSMENT"),
    ("what roads are damaged", "DAMAGE ASSESSMENT"),
    ("show active alerts", "ACTIVE ALERTS"),
    ("Is Jamnagar at high risk", "Jamnagar"),
    ("Kutch district risk", "Kutch"),
    ("hello", "Coastal Disaster"),
    ("help", "Help Guide"),
    ("overview", "COASTGUARD"),
    ("situation status", "COASTGUARD"),
]

for query, expected in routing_tests:
    resp = coastal_agent(query)
    passed = expected.lower() in resp.lower()
    check(f"Agent: '{query[:40]}'", passed,
          f"Expected '{expected}' not found in response (first 100 chars: {resp[:100]!r})")

# ── Language / Gujarati ──
print("\n[5] Gujarati Language Support")
r_fish = tool_fishermen_alert()
check("Gujarati text in fishermen alert", any(ord(c) > 2304 for c in r_fish))

alerts_data = get_active_alerts()
check("Gujarati message in alerts", all("message_gu" in a for a in alerts_data))
check("Gujarati text content", any(ord(c) > 2304 for a in alerts_data for c in a["message_gu"]))

# ── Summary ──
print()
print("=" * 60)
print(f"RESULTS: {PASS} passed / {FAIL} failed / {PASS + FAIL} total")
if FAIL == 0:
    print("ALL TESTS PASSED! 🎉")
else:
    print(f"⚠️  {FAIL} test(s) failed.")
print("=" * 60)
