# 🌀 CoastGuard AI — Smart Cyclone & Coastal Disaster Early Warning System
## Gujarat, India · IBM Granite AI + IBM Cloud + IBM Bob · Hackathon Prototype

> ⚠️ **DEMO DATA — Not for real emergency decision-making.**
> All data is simulated for prototype demonstration purposes only.

---

## 🎯 Project Goal

**One central AI agent** — the **Coastal Disaster Response Agent** — handles the complete cyclone disaster management workflow for Gujarat's coastal districts.

---

## 🤖 Central Agent: Coastal Disaster Response Agent

The agent understands the user's request and routes to the appropriate tool:

| Tool | Function |
|------|----------|
| **Tool 1** | 🌀 Cyclone Risk Analysis |
| **Tool 2** | 🚢 Fishermen Safety Alert |
| **Tool 3** | 🚗 Evacuation Planning |
| **Tool 4** | 🏥 Relief Resource Coordination |
| **Tool 5** | 🏚️ Post-Disaster Damage Assessment |

---

## 🚀 How to Run

### Install dependencies
```bash
pip install -r requirements.txt
```

### Launch CoastGuard AI
```bash
streamlit run coastguard_app.py
```

Opens at **http://localhost:8501**

---

## 🗂️ Project Structure

```
Coastal_Disaster_AI/
├── coastguard_app.py              # Main CoastGuard AI application (entry point)
├── requirements.txt               # Python dependencies
│
├── agent/
│   ├── coastal_agent.py           # Central Coastal Disaster Response Agent
│   │                              # (5 tools + intent detection + routing)
│   └── chat_engine.py             # Original SmartGuide chat (legacy)
│
├── data/
│   ├── disaster_data.py           # Gujarat coastal disaster DEMO data
│   │                              # (cyclone, districts, evacuation, relief, damage)
│   ├── gujarat_locations.json     # Location dataset (legacy)
│   ├── data_service.py            # Location data service (legacy)
│   ├── weather_service.py         # Weather service (legacy)
│   └── charts.py                  # Chart data (legacy)
│
└── ui/                            # Reserved for future UI components
```

---

## 🌊 Demo Scenario

**Cyclone VAYU** (Simulated)
- Wind Speed: 140 km/h
- Pressure: 950 hPa
- Distance from Coast: 180 km
- Movement: Northeast @ 14 km/h
- Affected Area: Saurashtra – Kutch coastline
- Risk Level: 🔴 CRITICAL

---

## 🗺️ Gujarat Coastal Districts Covered

| District | Risk Level | Pop at Risk |
|----------|-----------|-------------|
| Kutch | 🔴 Critical | 1,80,000 |
| Jamnagar | 🔴 Critical | 1,65,000 |
| Devbhumi Dwarka | 🔴 Critical | 95,000 |
| Porbandar | 🟠 High | 72,000 |
| Junagadh | 🟠 High | 58,000 |
| Gir Somnath | 🟠 High | 62,000 |
| Amreli | 🟡 Moderate | 38,000 |
| Bhavnagar | 🟡 Moderate | 42,000 |
| Bharuch | 🟡 Moderate | 22,000 |
| Surat | 🟢 Low | 15,000 |
| Navsari | 🟢 Low | 10,000 |
| Valsad | 🟢 Low | 8,000 |

---

## 🤖 How the AI Agent Works

1. **Intent Detection** — Regex pattern matching detects which disaster management function the user needs
2. **Tool Routing** — The agent routes to one of 5 specialised tools
3. **Structured Response** — Each tool generates a structured emergency-format response
4. **Language Support** — English + Gujarati alerts

### Chat Examples
```
"Analyse cyclone risk for Gujarat"       → Tool 1: Cyclone Risk Analysis
"Give fishermen safety alert"            → Tool 2: Fishermen Alert
"Which villages need to evacuate?"       → Tool 3: Evacuation Planning
"Show drinking water shortage in Kutch"  → Tool 4: Relief Coordination
"Show severe damage reports"             → Tool 5: Damage Assessment
"Is Jamnagar at high risk?"              → District Risk Check
"Show active alerts"                     → Active Alerts Panel
```

---

## 📊 Dashboard Pages

| Page | Description |
|------|-------------|
| **Emergency Dashboard** | Full command-center overview: cyclone status, risk, alerts, evacuation, relief, damage |
| **Cyclone Risk Analysis** | Interactive form + risk score calculator + district risk chart |
| **Fishermen Safety Alert** | Zone-specific alert generator in English + Gujarati |
| **Evacuation Planning** | Village-level evacuation plan with shelter capacity |
| **Relief Resources** | Resource inventory, shortage analysis, visual charts |
| **Damage Assessment** | Damage reports, severity filter, user report submission |
| **AI Agent Chat** | Conversational interface to the central agent |
| **Analytics** | Risk distribution, population charts, radar charts |

---

## 🛠️ Technologies

| Technology | Purpose |
|-----------|---------|
| **Python 3.11+** | Core language |
| **Streamlit 1.45** | Web UI framework |
| **Plotly 5.x** | Interactive charts |
| **Pandas** | Data manipulation |
| **IBM Granite LLM** | AI agent logic (prototype uses rule-based, production → IBM Granite) |
| **IBM Cloud** | Deployment platform |
| **IBM Bob** | Development environment |

---

## 🔌 How to Connect Real APIs

| Data Source | Replace Function In |
|-------------|-------------------|
| IMD (India Met Dept) live cyclone feed | `data/disaster_data.py → get_cyclone_data()` |
| NDMA resource inventory | `data/disaster_data.py → get_relief_resources()` |
| Gujarat SDMA shelter data | `data/disaster_data.py → get_evacuation_data()` |
| IMD district weather API | `data/weather_service.py` |
| IBM Granite LLM | `agent/coastal_agent.py → coastal_agent()` |

---

## ⚠️ Important Disclaimer

All data in this project is **DEMO/SIMULATED data** created for hackathon prototype demonstration only:
- Not real-time cyclone data
- Not official government evacuation orders
- Not actual shelter availability
- Not real emergency resource inventory
- Not affiliated with IMD, NDMA, or Gujarat SDMA

**The AI-generated estimates are prototype demonstrations — not official assessments.**

---

*🌀 CoastGuard AI — Built for IBM Hackathon using IBM Granite AI + IBM Cloud + IBM Bob*
*Focus: Gujarat Coastal Disaster Management | Smart Cyclone Early Warning System*
