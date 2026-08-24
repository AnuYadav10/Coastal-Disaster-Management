"""
CoastGuard AI — Smart Cyclone & Coastal Disaster Early Warning System
=======================================================================
Run with:  streamlit run coastguard_app.py

Central AI Agent: Coastal Disaster Response Agent
Powered by: IBM Granite LLM (logic layer) + IBM Cloud (deployment)
Focus: Gujarat, India coastal disaster management

⚠️  DEMO DATA — NOT for real emergency decision-making.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

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
    get_active_alerts,
    get_summary_stats,
)
from agent.coastal_agent import (
    coastal_agent,
    tool_cyclone_risk,
    tool_fishermen_alert,
    tool_evacuation_plan,
    tool_relief_coordination,
    tool_damage_assessment,
    RISK_COLOR,
)

# ─────────────────────────────────────────────
# Page Configuration
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="CoastGuard AI — Gujarat Cyclone Early Warning",
    page_icon="🌀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CSS Theme — Emergency Command Centre
# ─────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Background */
.stApp {
    background: linear-gradient(160deg, #060d1f 0%, #0a1628 40%, #06111e 100%);
    min-height: 100vh;
}

/* Header Banner */
.cg-header {
    background: linear-gradient(135deg, #0d1f3c 0%, #12284d 40%, #0a1e3b 100%);
    border: 1px solid rgba(56, 165, 255, 0.25);
    border-radius: 16px;
    padding: 24px 32px;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
}
.cg-header::before {
    content: '';
    position: absolute;
    top: -40%;
    right: -5%;
    width: 350px;
    height: 350px;
    background: radial-gradient(circle, rgba(56,165,255,0.08) 0%, transparent 65%);
    pointer-events: none;
}
.cg-title { font-size: 2.0rem; font-weight: 800; color: #fff; margin: 0; letter-spacing: -0.5px; }
.cg-subtitle { font-size: 0.92rem; color: rgba(255,255,255,0.65); margin: 4px 0 0 0; }
.cg-badge {
    display: inline-block;
    background: rgba(239, 68, 68, 0.15);
    color: #f87171;
    border: 1px solid rgba(239,68,68,0.35);
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-right: 6px;
    margin-top: 10px;
    display: inline-block;
}
.cg-badge-demo {
    display: inline-block;
    background: rgba(251,191,36,0.15);
    color: #fbbf24;
    border: 1px solid rgba(251,191,36,0.35);
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-right: 6px;
    margin-top: 10px;
    display: inline-block;
}
.cg-badge-ibm {
    display: inline-block;
    background: rgba(30, 100, 255, 0.18);
    color: #60a5fa;
    border: 1px solid rgba(30,100,255,0.35);
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-right: 6px;
    margin-top: 10px;
    display: inline-block;
}

/* Stat Cards */
.stat-card {
    background: linear-gradient(135deg, #111827 0%, #1a2234 100%);
    border: 1px solid rgba(56,165,255,0.15);
    border-radius: 12px;
    padding: 16px 18px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.stat-card.critical { border-color: rgba(239,68,68,0.4); background: linear-gradient(135deg, #1c0e0e 0%, #2a1111 100%); }
.stat-card.high { border-color: rgba(249,115,22,0.4); background: linear-gradient(135deg, #1c1308 0%, #291e0e 100%); }
.stat-card.moderate { border-color: rgba(245,158,11,0.35); background: linear-gradient(135deg, #141309 0%, #1e1c0d 100%); }
.stat-card.ok { border-color: rgba(34,197,94,0.3); background: linear-gradient(135deg, #0b160e 0%, #111e13 100%); }

.stat-num { font-size: 2rem; font-weight: 800; color: #38a5ff; margin: 0; line-height: 1; }
.stat-num.red { color: #f87171; }
.stat-num.orange { color: #fb923c; }
.stat-num.yellow { color: #fbbf24; }
.stat-num.green { color: #4ade80; }
.stat-label { font-size: 0.72rem; color: rgba(255,255,255,0.5); margin: 5px 0 0 0; text-transform: uppercase; letter-spacing: 0.6px; }

/* Risk Panel Cards */
.risk-card {
    background: #111827;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 10px;
    border-left: 4px solid #38a5ff;
}
.risk-card.critical { border-left-color: #ef4444; }
.risk-card.high { border-left-color: #f97316; }
.risk-card.moderate { border-left-color: #f59e0b; }
.risk-card.low { border-left-color: #22c55e; }
.risk-card-title { font-size: 0.95rem; font-weight: 700; color: #fff; margin: 0 0 4px 0; }
.risk-card-meta { font-size: 0.78rem; color: rgba(255,255,255,0.55); }
.risk-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.badge-critical { background: rgba(239,68,68,0.2); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }
.badge-high { background: rgba(249,115,22,0.2); color: #fb923c; border: 1px solid rgba(249,115,22,0.3); }
.badge-moderate { background: rgba(245,158,11,0.2); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); }
.badge-low { background: rgba(34,197,94,0.15); color: #4ade80; border: 1px solid rgba(34,197,94,0.25); }

/* Alert Cards */
.alert-card {
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 12px;
}
.alert-red { background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.35); }
.alert-orange { background: rgba(249,115,22,0.1); border: 1px solid rgba(249,115,22,0.35); }
.alert-yellow { background: rgba(245,158,11,0.1); border: 1px solid rgba(245,158,11,0.35); }
.alert-title { font-size: 0.9rem; font-weight: 700; color: #fff; margin: 0 0 6px 0; }
.alert-msg { font-size: 0.83rem; color: rgba(255,255,255,0.8); line-height: 1.55; margin-bottom: 8px; }
.alert-time { font-size: 0.72rem; color: rgba(255,255,255,0.45); }

/* Resource Bar */
.res-bar-container { width: 100%; background: rgba(255,255,255,0.07); border-radius: 4px; height: 8px; margin-top: 4px; }
.res-bar-fill { height: 8px; border-radius: 4px; transition: width 0.3s; }
.res-bar-ok { background: #4ade80; }
.res-bar-warn { background: #fbbf24; }
.res-bar-critical { background: #f87171; }

/* Chat */
.cg-chat-container {
    background: #0a1220;
    border: 1px solid rgba(56,165,255,0.15);
    border-radius: 16px;
    padding: 18px;
    max-height: 520px;
    overflow-y: auto;
}
.msg-user {
    background: linear-gradient(135deg, #1a3a5f, #1e4a70);
    border: 1px solid rgba(56,165,255,0.25);
    border-radius: 14px 14px 4px 14px;
    padding: 10px 14px;
    margin: 8px 0 8px 15%;
    color: #fff;
    font-size: 0.88rem;
    line-height: 1.5;
}
.msg-ai {
    background: #131e30;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px 14px 14px 4px;
    padding: 12px 16px;
    margin: 8px 15% 8px 0;
    color: rgba(255,255,255,0.9);
    font-size: 0.83rem;
    line-height: 1.65;
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    white-space: pre-wrap;
}
.lbl-user { font-size: 0.68rem; color: rgba(255,255,255,0.4); text-align: right; margin-bottom: 2px; }
.lbl-ai { font-size: 0.68rem; color: #38a5ff; margin-bottom: 2px; font-weight: 600; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #07101f 0%, #0a1628 100%);
    border-right: 1px solid rgba(56,165,255,0.12);
}
[data-testid="stSidebar"] .stMarkdown { color: rgba(255,255,255,0.85); }

/* Streamlit overrides */
.stTextInput > div > div > input {
    background: #111827 !important;
    border: 1px solid rgba(56,165,255,0.3) !important;
    border-radius: 10px !important;
    color: #fff !important;
    font-size: 0.9rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #38a5ff !important;
    box-shadow: 0 0 0 2px rgba(56,165,255,0.12) !important;
}
.stSelectbox > div > div {
    background: #111827 !important;
    border: 1px solid rgba(56,165,255,0.25) !important;
    border-radius: 10px !important;
}
.stButton > button {
    background: linear-gradient(135deg, #0d2044, #1a3a6e) !important;
    border: 1px solid rgba(56,165,255,0.35) !important;
    border-radius: 9px !important;
    color: #fff !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #1a3a6e, #22508c) !important;
    border-color: rgba(56,165,255,0.65) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: rgba(255,255,255,0.5);
    font-weight: 500;
    font-size: 0.88rem;
}
.stTabs [aria-selected="true"] {
    color: #38a5ff !important;
    border-bottom: 2px solid #38a5ff !important;
}
div[data-testid="stMetricValue"] { color: #38a5ff !important; font-weight: 800 !important; }

/* Section header */
.sec-hdr {
    font-size: 0.92rem;
    font-weight: 700;
    color: rgba(255,255,255,0.85);
    margin: 0 0 12px 0;
    padding-bottom: 7px;
    border-bottom: 1px solid rgba(56,165,255,0.15);
    display: flex;
    align-items: center;
    gap: 7px;
}

/* Demo Warning Banner */
.demo-banner {
    background: linear-gradient(90deg, rgba(251,191,36,0.12), rgba(251,191,36,0.06));
    border: 1px solid rgba(251,191,36,0.35);
    border-radius: 10px;
    padding: 10px 16px;
    color: rgba(251,191,36,0.95);
    font-size: 0.8rem;
    font-weight: 600;
    margin-bottom: 14px;
    text-align: center;
    letter-spacing: 0.3px;
}

/* Scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.03); }
::-webkit-scrollbar-thumb { background: rgba(56,165,255,0.35); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(56,165,255,0.65); }

/* Dataframe override */
.stDataFrame { background: #111827 !important; }

/* Progress / Resource table */
.res-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 5px 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    font-size: 0.82rem;
}
.res-name { width: 160px; color: rgba(255,255,255,0.75); }
.res-val { width: 60px; text-align: right; font-weight: 600; font-family: 'JetBrains Mono', monospace; }

.cyclone-stat {
    background: rgba(239,68,68,0.08);
    border: 1px solid rgba(239,68,68,0.2);
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 8px;
}
.cyclone-stat-label { font-size: 0.7rem; color: rgba(255,255,255,0.45); text-transform: uppercase; letter-spacing: 0.6px; }
.cyclone-stat-value { font-size: 1.35rem; font-weight: 700; color: #f87171; }

.damage-row {
    background: #111827;
    border-radius: 8px;
    padding: 12px 14px;
    margin-bottom: 8px;
    border-left: 3px solid #f97316;
}
.damage-row.critical { border-left-color: #ef4444; }
.damage-row.severe { border-left-color: #f97316; }
.damage-row.moderate { border-left-color: #f59e0b; }
.damage-row.minor { border-left-color: #22c55e; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Session State
# ─────────────────────────────────────────────

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "lang" not in st.session_state:
    st.session_state.lang = "English"
if "active_tool" not in st.session_state:
    st.session_state.active_tool = None

# ─────────────────────────────────────────────
# Helper: Risk badge HTML
# ─────────────────────────────────────────────

def risk_badge(level: str) -> str:
    cls = level.lower()
    return f'<span class="risk-badge badge-{cls}">{level}</span>'


def severity_badge(sev: str) -> str:
    cls = sev.lower()
    return f'<span class="risk-badge badge-{cls}">{sev}</span>'


# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:14px 0 20px 0;">
        <div style="font-size:2.8rem;">🌀</div>
        <div style="font-size:1.05rem; font-weight:800; color:#fff; margin-top:6px;">CoastGuard AI</div>
        <div style="font-size:0.72rem; color:rgba(255,255,255,0.45); margin-top:3px;">Gujarat Cyclone Early Warning</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div style="font-size:0.72rem; font-weight:700; color:rgba(255,255,255,0.45); text-transform:uppercase; letter-spacing:1px; margin-bottom:8px;">Navigation</div>', unsafe_allow_html=True)

    nav_opts = [
        "🏠 Emergency Dashboard",
        "🌀 Cyclone Risk Analysis",
        "🚢 Fishermen Safety Alert",
        "🚗 Evacuation Planning",
        "🏥 Relief Resources",
        "🏚️ Damage Assessment",
        "🤖 AI Agent Chat",
        "📊 Analytics",
    ]
    nav = st.radio("", nav_opts, label_visibility="collapsed")

    st.markdown("---")
    st.markdown("**🌐 Language / ભાષા**")
    lang = st.selectbox("", ["English", "Gujarati / ગુજરાતી"], label_visibility="collapsed", key="lang_select")
    st.session_state.lang = lang.split(" ")[0]

    st.markdown("---")
    stats = get_summary_stats()
    st.markdown(f"""
    <div style="font-size:0.76rem; color:rgba(255,255,255,0.5);">
        <div style="margin-bottom:5px;">🔴 <strong style="color:#f87171;">Critical Districts: {stats['critical_districts']}</strong></div>
        <div style="margin-bottom:5px;">🟠 <strong style="color:#fb923c;">High Risk: {stats['high_districts']}</strong></div>
        <div style="margin-bottom:5px;">👥 Population at Risk: <strong style="color:#38a5ff;">{stats['total_pop_at_risk']:,}</strong></div>
        <div style="margin-bottom:5px;">🔔 Active Alerts: <strong style="color:#fbbf24;">{stats['active_alerts']}</strong></div>
        <div style="margin-bottom:5px;">🌀 Cyclone: <strong style="color:#f87171;">{stats['cyclone_name']}</strong></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="background:rgba(251,191,36,0.08); border:1px solid rgba(251,191,36,0.25); border-radius:8px; padding:9px 12px; font-size:0.72rem; color:rgba(251,191,36,0.9);">
        ⚠️ <strong>DEMO DATA</strong><br>
        Not for real emergency decision-making.<br>
        Powered by IBM Granite AI + IBM Cloud
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────

cy = get_cyclone_data()
stats = get_summary_stats()

st.markdown(f"""
<div class="cg-header">
    <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px;">
        <div>
            <h1 class="cg-title">🌀 CoastGuard AI</h1>
            <p class="cg-subtitle">Smart Cyclone & Coastal Disaster Early Warning System — Gujarat, India</p>
            <div style="margin-top:10px;">
                <span class="cg-badge">🔴 ACTIVE CYCLONE</span>
                <span class="cg-badge-demo">⚠️ DEMO DATA</span>
                <span class="cg-badge-ibm">IBM Granite AI</span>
            </div>
        </div>
        <div style="text-align:right;">
            <div style="font-size:0.75rem; color:rgba(255,255,255,0.4); margin-bottom:4px;">Active Scenario</div>
            <div style="font-size:1.2rem; font-weight:700; color:#f87171;">{cy['name']}</div>
            <div style="font-size:0.82rem; color:rgba(255,255,255,0.6);">{cy['wind_speed_kmh']} km/h · {cy['pressure_hpa']} hPa · {cy['distance_from_coast_km']} km from coast</div>
            <div style="font-size:0.72rem; color:rgba(255,255,255,0.35); margin-top:4px;">{cy['last_updated']}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Demo data banner
st.markdown("""
<div class="demo-banner">
    ⚠️  DEMO DATA – This application uses SIMULATED data for prototype demonstration.
    NOT for real emergency decision-making. Do not issue official warnings based on this system.
</div>
""", unsafe_allow_html=True)

# Top stats row
c1, c2, c3, c4, c5, c6, c7, c8 = st.columns(8)
stat_configs = [
    ("🌀", stats["cyclone_wind_speed"], "Wind km/h", "red", "critical"),
    ("🔴", stats["critical_districts"], "Critical Districts", "red", "critical"),
    ("🟠", stats["high_districts"], "High Risk", "orange", "high"),
    ("👥", f"{stats['total_pop_at_risk']//1000}K", "People at Risk", "yellow", "moderate"),
    ("🏘️", stats["total_villages_at_risk"], "Villages at Risk", "orange", "high"),
    ("🔔", stats["active_alerts"], "Active Alerts", "red", "critical"),
    ("🚗", stats["evacuation_villages"], "Evacuation Sites", "yellow", "moderate"),
    ("🏚️", stats["damage_reports"], "Damage Reports", "orange", "high"),
]
cols = [c1, c2, c3, c4, c5, c6, c7, c8]
for col, (icon, val, label, color_cls, card_cls) in zip(cols, stat_configs):
    with col:
        st.markdown(f"""
        <div class="stat-card {card_cls}">
            <div style="font-size:1.3rem;">{icon}</div>
            <p class="stat-num {color_cls}">{val}</p>
            <p class="stat-label">{label}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Page Router
# ─────────────────────────────────────────────

page = nav.split(" ", 1)[1].strip()

# ══════════════════════════════════════════════
# PAGE: Emergency Dashboard
# ══════════════════════════════════════════════
if "Emergency Dashboard" in page:
    left_col, mid_col, right_col = st.columns([1.2, 1.2, 1])

    # ── LEFT: Cyclone Status + Coastal Risk
    with left_col:
        # Cyclone status
        st.markdown('<div class="sec-hdr">🌀 Cyclone Status</div>', unsafe_allow_html=True)
        cy_fields = [
            ("Cyclone Name", cy["name"]),
            ("Category", cy["category"]),
            ("Location", f"{cy['lat']}°N, {cy['lon']}°E"),
            ("Wind Speed", f"{cy['wind_speed_kmh']} km/h"),
            ("Pressure", f"{cy['pressure_hpa']} hPa"),
            ("Movement", f"{cy['movement_direction']} @ {cy['movement_speed_kmh']} km/h"),
            ("Distance", f"{cy['distance_from_coast_km']} km from coast"),
            ("Rainfall", f"{cy.get('rainfall_mm', 85)} mm"),
        ]
        cols_data = [cy_fields[:4], cy_fields[4:]]
        cya, cyb = st.columns(2)
        for field, val in cy_fields[:4]:
            cya.markdown(f"""
            <div class="cyclone-stat">
                <div class="cyclone-stat-label">{field}</div>
                <div class="cyclone-stat-value">{val}</div>
            </div>""", unsafe_allow_html=True)
        for field, val in cy_fields[4:]:
            cyb.markdown(f"""
            <div class="cyclone-stat">
                <div class="cyclone-stat-label">{field}</div>
                <div class="cyclone-stat-value" style="font-size:1.1rem; color:#fbbf24;">{val}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        # Coastal Risk
        st.markdown('<div class="sec-hdr">🗺️ Coastal Risk by District</div>', unsafe_allow_html=True)
        districts = get_coastal_districts()
        risk_order = {"Critical": 0, "High": 1, "Moderate": 2, "Low": 3}
        districts_sorted = sorted(districts, key=lambda x: risk_order.get(x["risk_level"], 4))

        for d in districts_sorted[:8]:
            rl = d["risk_level"]
            st.markdown(f"""
            <div class="risk-card {rl.lower()}">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div class="risk-card-title">{d['name']}</div>
                        <div class="risk-card-meta">Villages: {d['villages_at_risk']} · Pop at risk: {d['pop_at_risk']:,}</div>
                    </div>
                    {risk_badge(rl)}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── MID: Alerts + Evacuation
    with mid_col:
        # Active Alerts
        st.markdown('<div class="sec-hdr">🔔 Active Alerts</div>', unsafe_allow_html=True)
        alerts = get_active_alerts()
        alert_class_map = {"RED": "alert-red", "ORANGE": "alert-orange", "YELLOW": "alert-yellow"}
        for a in alerts:
            acls = alert_class_map.get(a["level"], "alert-yellow")
            if st.session_state.lang == "Gujarati":
                msg = a["message_gu"]
            else:
                msg = a["message_en"]
            st.markdown(f"""
            <div class="alert-card {acls}">
                <div class="alert-title">{RISK_COLOR.get(a['level'], '⚪')} [{a['level']}] {a['type']}</div>
                <div class="alert-msg">{a['area']}</div>
                <div class="alert-msg">{msg}</div>
                <div class="alert-time">{a['issued_time']} · {a['authority']}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        # Evacuation Summary
        st.markdown('<div class="sec-hdr">🚗 Evacuation Priority</div>', unsafe_allow_html=True)
        evac_list = get_priority_evacuations(["Critical", "High"])[:5]
        for e in evac_list:
            rl = e["risk_level"]
            cap_free = e["shelter_capacity"] - e["shelter_occupancy"]
            cap_icon = "✅" if cap_free >= e["population"] else "⚠️"
            st.markdown(f"""
            <div class="risk-card {rl.lower()}">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                        <div class="risk-card-title">#{e['priority']} {e['village']}, {e['district']}</div>
                        <div class="risk-card-meta">👥 {e['population']:,} people · 🏫 {e['shelter']}</div>
                        <div class="risk-card-meta">{cap_icon} Shelter free: {cap_free} · {e['distance_km']} km</div>
                    </div>
                    {risk_badge(rl)}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── RIGHT: Relief + Damage
    with right_col:
        # Relief Overview
        st.markdown('<div class="sec-hdr">🏥 Relief Resources</div>', unsafe_allow_html=True)
        shortages = get_resource_shortages()

        # Summary resource bar chart
        res_names = ["Food", "Water", "Medicine", "Rescue\nTeams", "Boats"]
        res_keys = ["food_packets", "drinking_water_liters", "medicines_kits", "rescue_teams", "rescue_boats"]

        for rel in get_relief_resources()[:2]:
            rl = rel["risk_level"]
            st.markdown(f'<div style="font-size:0.78rem; font-weight:600; color:#fff; margin-bottom:5px;">{RISK_COLOR.get(rl,"⚪")} {rel["location"]}</div>', unsafe_allow_html=True)
            for rk, rn in zip(res_keys, res_names):
                qty = rel["resources"][rk]
                avail, req = qty["available"], qty["required"]
                pct = min(100, int(avail / req * 100)) if req > 0 else 100
                bar_cls = "res-bar-ok" if pct >= 80 else ("res-bar-warn" if pct >= 40 else "res-bar-critical")
                st.markdown(f"""
                <div style="margin-bottom:4px;">
                    <div style="display:flex; justify-content:space-between; font-size:0.72rem; color:rgba(255,255,255,0.6);">
                        <span>{rn.replace(chr(10),' ')}</span>
                        <span>{avail:,}/{req:,}</span>
                    </div>
                    <div class="res-bar-container"><div class="res-bar-fill {bar_cls}" style="width:{pct}%;"></div></div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        # Damage Summary
        st.markdown('<div class="sec-hdr">🏚️ Damage Reports</div>', unsafe_allow_html=True)
        dmg_reports = get_damage_reports()
        sev_icons = {"Critical": "🔴", "Severe": "🟠", "Moderate": "🟡", "Minor": "🟢"}
        for r in sorted(dmg_reports, key=lambda x: x["priority"])[:4]:
            sev_cls = r["severity"].lower()
            si = sev_icons.get(r["severity"], "⚪")
            st.markdown(f"""
            <div class="damage-row {sev_cls}">
                <div style="font-size:0.82rem; font-weight:600; color:#fff;">{si} {r['damage_type']} — {r['district']}</div>
                <div style="font-size:0.73rem; color:rgba(255,255,255,0.55); margin-top:3px;">{r['location']}</div>
                <div style="font-size:0.73rem; color:rgba(255,255,255,0.5); margin-top:2px;">👥 {r['affected_people']:,} affected · {r['source']}</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# PAGE: Cyclone Risk Analysis
# ══════════════════════════════════════════════
elif "Cyclone Risk" in page:
    st.markdown('<div class="sec-hdr">🌀 Cyclone Risk Analysis — Tool 1</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:rgba(56,165,255,0.07); border:1px solid rgba(56,165,255,0.2); border-radius:10px; padding:12px 16px; font-size:0.82rem; color:rgba(255,255,255,0.75); margin-bottom:16px;">
        The <strong>Coastal Disaster Response Agent</strong> analyses cyclone parameters and calculates a prototype risk score (0–100).
        Adjust parameters below and click <strong>Analyse Risk</strong> to get a full report.
    </div>
    """, unsafe_allow_html=True)

    cy_data = get_cyclone_data()

    with st.form("cyclone_form"):
        st.markdown("**Cyclone Parameters (DEMO — Pre-filled with active scenario)**")
        cc1, cc2, cc3 = st.columns(3)
        with cc1:
            cy_name = st.text_input("Cyclone Name", value=cy_data["name"])
            wind_speed = st.number_input("Wind Speed (km/h)", min_value=0, max_value=350, value=int(cy_data["wind_speed_kmh"]))
            pressure = st.number_input("Atmospheric Pressure (hPa)", min_value=850, max_value=1050, value=int(cy_data["pressure_hpa"]))
        with cc2:
            lat = st.number_input("Latitude (°N)", min_value=15.0, max_value=30.0, value=float(cy_data["lat"]), format="%.2f")
            lon = st.number_input("Longitude (°E)", min_value=60.0, max_value=80.0, value=float(cy_data["lon"]), format="%.2f")
            rainfall = st.number_input("Rainfall (mm)", min_value=0, max_value=500, value=int(cy_data.get("rainfall_mm", 85)))
        with cc3:
            movement_dir = st.selectbox("Movement Direction", ["Northeast", "North", "Northwest", "East", "West", "South"], index=0)
            movement_speed = st.number_input("Movement Speed (km/h)", min_value=0, max_value=60, value=int(cy_data["movement_speed_kmh"]))
            distance = st.number_input("Distance from Coast (km)", min_value=0, max_value=1000, value=int(cy_data["distance_from_coast_km"]))

        affected_area = st.text_input("Affected Coastal Area", value=cy_data["affected_coastal_area"])
        analyse = st.form_submit_button("🌀 Analyse Cyclone Risk", use_container_width=True)

    if analyse:
        params = {
            "name": cy_name,
            "lat": lat,
            "lon": lon,
            "wind_speed_kmh": wind_speed,
            "pressure_hpa": pressure,
            "rainfall_mm": rainfall,
            "movement_direction": movement_dir,
            "movement_speed_kmh": movement_speed,
            "distance_from_coast_km": distance,
            "affected_coastal_area": affected_area,
        }
        result = tool_cyclone_risk(params)
        st.markdown(f"""
        <div style="background:#0a1220; border:1px solid rgba(56,165,255,0.2); border-radius:12px; padding:18px; font-family:'JetBrains Mono',monospace; font-size:0.83rem; color:rgba(255,255,255,0.9); white-space:pre-wrap; line-height:1.7;">
{result}
        </div>
        """, unsafe_allow_html=True)

    # Always show the district risk chart
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="sec-hdr">📊 District Risk Overview</div>', unsafe_allow_html=True)

    districts = get_coastal_districts()
    df_d = pd.DataFrame({
        "District": [d["name"] for d in districts],
        "Pop at Risk": [d["pop_at_risk"] for d in districts],
        "Villages at Risk": [d["villages_at_risk"] for d in districts],
        "Risk Level": [d["risk_level"] for d in districts],
    })

    color_map = {"Critical": "#ef4444", "High": "#f97316", "Moderate": "#f59e0b", "Low": "#22c55e"}
    fig = px.bar(
        df_d, x="District", y="Pop at Risk",
        color="Risk Level",
        color_discrete_map=color_map,
        title="Population at Risk by Coastal District (DEMO DATA)",
        template="plotly_dark",
        text="Pop at Risk",
    )
    fig.update_traces(texttemplate='%{text:,}', textposition='outside', textfont_size=8)
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="rgba(255,255,255,0.8)", size=11),
        xaxis_tickangle=-30, height=380,
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════
# PAGE: Fishermen Safety Alert
# ══════════════════════════════════════════════
elif "Fishermen" in page:
    st.markdown('<div class="sec-hdr">🚢 Fishermen Safety Alert — Tool 2</div>', unsafe_allow_html=True)

    fa1, fa2 = st.columns([2, 1])
    with fa1:
        selected_zone = st.selectbox(
            "Select Fishing Zone (or All)",
            ["All Gujarat Fishing Zones", "Gulf of Kutch Zone A", "Gulf of Kutch Zone B",
             "Jamnagar Coastal Zone", "Marine National Park Zone", "Porbandar Deep Sea Zone",
             "Veraval Zone", "Somnath Zone", "Dwarka Fishing Zone", "Okha Zone"],
            key="zone_select"
        )
        sel_lang = st.radio("Alert Language", ["English", "Gujarati", "Both"], horizontal=True, key="fish_lang")

    with fa2:
        gen_alert = st.button("🚨 Generate Fishermen Alert", key="gen_fish_alert", use_container_width=True)
        st.markdown("""
        <div class="alert-card alert-red" style="margin-top:8px;">
            <div class="alert-title">🔴 Current Status</div>
            <div class="alert-msg">Cyclone VAYU — 180 km from coast<br>Wind: 140 km/h · CRITICAL</div>
        </div>
        """, unsafe_allow_html=True)

    if gen_alert or not st.session_state.active_tool:
        zone_param = None if "All" in selected_zone else selected_zone
        result = tool_fishermen_alert(zone_param)
        st.session_state.active_tool = "fish"

        st.markdown(f"""
        <div style="background:#0a1220; border:1px solid rgba(239,68,68,0.3); border-radius:12px; padding:18px; font-family:'JetBrains Mono',monospace; font-size:0.83rem; color:rgba(255,255,255,0.9); white-space:pre-wrap; line-height:1.7; margin-top:12px;">
{result}
        </div>
        """, unsafe_allow_html=True)
    else:
        result = tool_fishermen_alert()
        st.markdown(f"""
        <div style="background:#0a1220; border:1px solid rgba(239,68,68,0.3); border-radius:12px; padding:18px; font-family:'JetBrains Mono',monospace; font-size:0.83rem; color:rgba(255,255,255,0.9); white-space:pre-wrap; line-height:1.7; margin-top:12px;">
{result}
        </div>
        """, unsafe_allow_html=True)

    # Fishing zone risk table
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="sec-hdr">🎣 Fishing Zone Risk Matrix</div>', unsafe_allow_html=True)

    zone_data = []
    for d in get_coastal_districts():
        for z in d["fishing_zones"]:
            zone_data.append({
                "Fishing Zone": z,
                "District": d["name"],
                "Risk Level": d["risk_level"],
                "Status": "⛔ CLOSED" if d["risk_level"] in ("Critical", "High") else ("⚠️ RESTRICTED" if d["risk_level"] == "Moderate" else "✅ CAUTION"),
                "Coastal Length (km)": d["coastal_length_km"],
            })
    df_zones = pd.DataFrame(zone_data)
    st.dataframe(df_zones, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════
# PAGE: Evacuation Planning
# ══════════════════════════════════════════════
elif "Evacuation" in page:
    st.markdown('<div class="sec-hdr">🚗 Evacuation Planning — Tool 3</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:rgba(249,115,22,0.07); border:1px solid rgba(249,115,22,0.2); border-radius:10px; padding:12px 16px; font-size:0.82rem; color:rgba(255,255,255,0.75); margin-bottom:16px;">
        ⚠️ Routes shown are SIMULATED for demo purposes. Do NOT treat these as official evacuation routes.
    </div>
    """, unsafe_allow_html=True)

    ev1, ev2, ev3 = st.columns([1, 1, 1])
    with ev1:
        ev_district = st.selectbox("Filter by District", ["All Districts"] + [d["name"] for d in get_coastal_districts()], key="ev_dist")
    with ev2:
        ev_risk = st.multiselect("Risk Levels", ["Critical", "High", "Moderate"], default=["Critical", "High"], key="ev_risk")
    with ev3:
        gen_evac = st.button("🚗 Generate Evacuation Plan", use_container_width=True, key="gen_evac")

    if gen_evac or True:
        dist_param = None if ev_district == "All Districts" else ev_district
        result = tool_evacuation_plan(dist_param, ev_risk if ev_risk else None)
        st.markdown(f"""
        <div style="background:#0a1220; border:1px solid rgba(249,115,22,0.25); border-radius:12px; padding:18px; font-family:'JetBrains Mono',monospace; font-size:0.83rem; color:rgba(255,255,255,0.9); white-space:pre-wrap; line-height:1.7; margin-top:10px;">
{result}
        </div>
        """, unsafe_allow_html=True)

    # Shelter capacity chart
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="sec-hdr">🏫 Shelter Capacity Overview</div>', unsafe_allow_html=True)

    evac_all = get_evacuation_data()
    df_evac = pd.DataFrame({
        "Shelter": [e["shelter"][:30] + "…" if len(e["shelter"]) > 30 else e["shelter"] for e in evac_all],
        "Capacity": [e["shelter_capacity"] for e in evac_all],
        "Occupied": [e["shelter_occupancy"] for e in evac_all],
        "Free": [e["shelter_capacity"] - e["shelter_occupancy"] for e in evac_all],
        "Population Needed": [e["population"] for e in evac_all],
        "Village": [e["village"] for e in evac_all],
        "Risk": [e["risk_level"] for e in evac_all],
    })

    fig_evac = go.Figure()
    fig_evac.add_bar(name="Occupied", x=df_evac["Shelter"], y=df_evac["Occupied"], marker_color="#f97316")
    fig_evac.add_bar(name="Free Capacity", x=df_evac["Shelter"], y=df_evac["Free"], marker_color="#38a5ff")
    fig_evac.update_layout(
        barmode="stack",
        title="Shelter Capacity vs Current Occupancy (DEMO DATA)",
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="rgba(255,255,255,0.8)", size=10),
        xaxis_tickangle=-30, height=350,
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    st.plotly_chart(fig_evac, use_container_width=True)


# ══════════════════════════════════════════════
# PAGE: Relief Resources
# ══════════════════════════════════════════════
elif "Relief" in page:
    st.markdown('<div class="sec-hdr">🏥 Relief Resource Coordination — Tool 4</div>', unsafe_allow_html=True)

    rr1, rr2, rr3 = st.columns([1.5, 1.5, 1])
    with rr1:
        rr_district = st.selectbox("Filter by District", ["All Districts"] + [r["district"] for r in get_relief_resources()], key="rr_dist")
    with rr2:
        rr_resource = st.selectbox("Filter by Resource Type",
            ["All Resources", "food_packets", "drinking_water_liters", "medicines_kits",
             "rescue_teams", "rescue_boats", "emergency_shelters", "medical_teams"],
            key="rr_res")
    with rr3:
        gen_relief = st.button("🏥 Generate Relief Report", use_container_width=True, key="gen_relief")

    dist_param = None if rr_district == "All Districts" else rr_district
    res_param = None if rr_resource == "All Resources" else rr_resource
    result = tool_relief_coordination(dist_param, res_param)
    st.markdown(f"""
    <div style="background:#0a1220; border:1px solid rgba(34,197,94,0.2); border-radius:12px; padding:18px; font-family:'JetBrains Mono',monospace; font-size:0.83rem; color:rgba(255,255,255,0.9); white-space:pre-wrap; line-height:1.7; margin-top:10px;">
{result}
    </div>
    """, unsafe_allow_html=True)

    # Resource shortage visual
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="sec-hdr">📊 Resource Availability — Critical Areas</div>', unsafe_allow_html=True)

    rel_data = get_relief_resources()
    resource_labels = {
        "food_packets": "Food Packets",
        "drinking_water_liters": "Water (L)",
        "medicines_kits": "Medicine Kits",
        "rescue_teams": "Rescue Teams",
        "rescue_boats": "Rescue Boats",
        "emergency_shelters": "Shelters",
        "medical_teams": "Medical Teams",
    }

    rows = []
    for entry in rel_data:
        for rk, rl in resource_labels.items():
            qty = entry["resources"][rk]
            rows.append({
                "Location": entry["location"][:20],
                "Resource": rl,
                "Available": qty["available"],
                "Required": qty["required"],
                "Shortage": max(0, qty["required"] - qty["available"]),
                "Pct Available": round(qty["available"] / qty["required"] * 100, 1) if qty["required"] > 0 else 100,
            })
    df_rel = pd.DataFrame(rows)

    fig_rel = px.bar(
        df_rel[df_rel["Shortage"] > 0].head(20),
        x="Resource", y="Shortage",
        color="Location",
        barmode="group",
        title="Resource Shortages by Location and Type (DEMO DATA)",
        template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Set1,
    )
    fig_rel.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="rgba(255,255,255,0.8)", size=10),
        height=380, legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    st.plotly_chart(fig_rel, use_container_width=True)


# ══════════════════════════════════════════════
# PAGE: Damage Assessment
# ══════════════════════════════════════════════
elif "Damage" in page:
    st.markdown('<div class="sec-hdr">🏚️ Post-Disaster Damage Assessment — Tool 5</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:rgba(239,68,68,0.07); border:1px solid rgba(239,68,68,0.2); border-radius:10px; padding:12px 16px; font-size:0.82rem; color:rgba(255,255,255,0.75); margin-bottom:16px;">
        ⚠️ AI-generated estimates based on SIMULATED data. Not official government damage assessments.
    </div>
    """, unsafe_allow_html=True)

    dm1, dm2, dm3 = st.columns([1, 1.5, 1])
    with dm1:
        dm_severity = st.selectbox("Filter by Severity", ["All Severities", "Critical", "Severe", "Moderate", "Minor"], key="dm_sev")
    with dm2:
        dm_district = st.selectbox("Filter by District", ["All Districts"] + [d["name"] for d in get_coastal_districts()], key="dm_dist")
    with dm3:
        gen_dmg = st.button("🏚️ Generate Damage Report", use_container_width=True, key="gen_dmg")

    sev_param = None if dm_severity == "All Severities" else dm_severity
    dist_param_dm = None if dm_district == "All Districts" else dm_district
    result = tool_damage_assessment(sev_param, dist_param_dm)
    st.markdown(f"""
    <div style="background:#0a1220; border:1px solid rgba(239,68,68,0.25); border-radius:12px; padding:18px; font-family:'JetBrains Mono',monospace; font-size:0.83rem; color:rgba(255,255,255,0.9); white-space:pre-wrap; line-height:1.7; margin-top:10px;">
{result}
    </div>
    """, unsafe_allow_html=True)

    # Report new damage
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="sec-hdr">📝 Submit Damage Report (User Input)</div>', unsafe_allow_html=True)

    with st.form("damage_form"):
        df1, df2 = st.columns(2)
        with df1:
            rep_location = st.text_input("Affected Location", placeholder="e.g. Maska Village, Kutch")
            rep_type = st.selectbox("Damage Type", ["Houses", "Roads", "Bridges", "Boats & Fishing", "Electricity", "Agricultural Land", "Public Infrastructure"])
            rep_severity = st.selectbox("Severity", ["Minor", "Moderate", "Severe", "Critical"])
        with df2:
            rep_people = st.number_input("Estimated Affected People", min_value=0, max_value=100000, value=0)
            rep_desc = st.text_area("Damage Description", placeholder="Describe what was damaged and the extent of damage…", height=100)
        submit_dmg = st.form_submit_button("📤 Submit Damage Report", use_container_width=True)

    if submit_dmg and rep_location and rep_desc:
        sev_icons2 = {"Critical": "🔴", "Severe": "🟠", "Moderate": "🟡", "Minor": "🟢"}
        si = sev_icons2.get(rep_severity, "⚪")
        st.success(f"""
✅ **Damage Report Submitted (DEMO)**

{si} **Location:** {rep_location}
**Damage Type:** {rep_type}
**Severity:** {rep_severity}
**Affected People:** {rep_people:,}
**Description:** {rep_desc}

*This is a demo submission. In a real system, this would be logged to the emergency database.*
        """)

    # Severity distribution chart
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="sec-hdr">📊 Damage Severity Distribution</div>', unsafe_allow_html=True)

    damage_all = get_damage_reports()
    sev_counts = {}
    for r in damage_all:
        sev_counts[r["severity"]] = sev_counts.get(r["severity"], 0) + 1

    fig_dmg = px.pie(
        names=list(sev_counts.keys()),
        values=list(sev_counts.values()),
        title="Damage Reports by Severity (DEMO DATA)",
        template="plotly_dark",
        color_discrete_map={"Critical": "#ef4444", "Severe": "#f97316", "Moderate": "#f59e0b", "Minor": "#22c55e"},
        hole=0.4,
    )
    fig_dmg.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="rgba(255,255,255,0.8)"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        height=300,
    )
    st.plotly_chart(fig_dmg, use_container_width=True)


# ══════════════════════════════════════════════
# PAGE: AI Agent Chat
# ══════════════════════════════════════════════
elif "AI Agent Chat" in page:
    st.markdown('<div class="sec-hdr">🤖 Coastal Disaster Response Agent — AI Chat</div>', unsafe_allow_html=True)

    chat_main, chat_side = st.columns([2.2, 1])

    with chat_main:
        # Welcome message on first load
        if not st.session_state.chat_history:
            welcome = coastal_agent("hello")
            st.session_state.chat_history.append({"role": "assistant", "content": welcome})

        # Chat history
        st.markdown('<div class="cg-chat-container">', unsafe_allow_html=True)
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div style="text-align:right;">
                    <div class="lbl-user">You</div>
                    <div class="msg-user">{msg['content']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div>
                    <div class="lbl-ai">🌀 Coastal Disaster Response Agent</div>
                    <div class="msg-ai">{msg['content']}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        # Input form
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input(
                "",
                placeholder="Ask the AI agent… e.g. 'Which villages need to evacuate?' or 'Show relief shortages'",
                key="chat_input",
                label_visibility="collapsed"
            )
            sc1, sc2 = st.columns([3, 1])
            with sc1:
                send = st.form_submit_button("📤 Send", use_container_width=True)
            with sc2:
                clear = st.form_submit_button("🗑️ Clear", use_container_width=True)

        if send and user_input.strip():
            st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})
            response = coastal_agent(user_input.strip())
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()

        if clear:
            st.session_state.chat_history = []
            st.rerun()

    with chat_side:
        st.markdown('<div class="sec-hdr">💡 Quick Queries</div>', unsafe_allow_html=True)

        sample_qs = [
            "Analyse cyclone risk for Gujarat",
            "Give fishermen safety alert",
            "Which villages need to evacuate?",
            "Which shelters have free capacity?",
            "Show drinking water shortage",
            "Show severe damage reports",
            "Is Jamnagar at high risk?",
            "Show Kutch damage reports",
            "Generate Gujarati alert",
            "Show all active alerts",
            "Relief resources for Dwarka",
            "Overview situation",
        ]
        for q in sample_qs:
            if st.button(f"💬 {q}", key=f"sq_{q[:25]}", use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": q})
                resp = coastal_agent(q)
                st.session_state.chat_history.append({"role": "assistant", "content": resp})
                st.rerun()

        st.markdown("---")
        st.markdown("""
        <div style="background:rgba(30,100,255,0.08); border:1px solid rgba(30,100,255,0.2); border-radius:8px; padding:10px 12px; font-size:0.72rem; color:rgba(255,255,255,0.65);">
            🤖 <strong>IBM Granite AI</strong><br>
            Central agent routes your request to the appropriate disaster management tool.<br><br>
            ⚠️ DEMO DATA — Simulated scenario
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# PAGE: Analytics
# ══════════════════════════════════════════════
elif "Analytics" in page:
    st.markdown('<div class="sec-hdr">📊 Disaster Analytics Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div style="background:rgba(251,191,36,0.08); border:1px solid rgba(251,191,36,0.2); border-radius:8px; padding:8px 14px; font-size:0.78rem; color:rgba(251,191,36,0.85); margin-bottom:14px;">⚠️ All charts use DEMO/SIMULATED data for prototype demonstration.</div>', unsafe_allow_html=True)

    an1, an2 = st.columns(2)

    with an1:
        # Risk distribution pie
        districts = get_coastal_districts()
        risk_counts = {}
        for d in districts:
            risk_counts[d["risk_level"]] = risk_counts.get(d["risk_level"], 0) + 1

        fig_risk = px.pie(
            names=list(risk_counts.keys()),
            values=list(risk_counts.values()),
            title="Coastal Districts by Risk Level",
            template="plotly_dark",
            color_discrete_map={"Critical": "#ef4444", "High": "#f97316", "Moderate": "#f59e0b", "Low": "#22c55e"},
            hole=0.4,
        )
        fig_risk.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="rgba(255,255,255,0.8)"),
            legend=dict(bgcolor="rgba(0,0,0,0)"),
            height=320,
        )
        st.plotly_chart(fig_risk, use_container_width=True)

    with an2:
        # Coastal population at risk bar
        high_d = sorted(
            [d for d in districts if d["risk_level"] in ("Critical", "High")],
            key=lambda x: x["pop_at_risk"], reverse=True
        )
        fig_pop = px.bar(
            x=[d["name"] for d in high_d],
            y=[d["pop_at_risk"] for d in high_d],
            color=[d["risk_level"] for d in high_d],
            color_discrete_map={"Critical": "#ef4444", "High": "#f97316"},
            title="Population at Risk — Critical & High Districts",
            template="plotly_dark",
            labels={"x": "District", "y": "Population at Risk", "color": "Risk Level"},
        )
        fig_pop.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="rgba(255,255,255,0.8)", size=10),
            height=320, xaxis_tickangle=-20,
            legend=dict(bgcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig_pop, use_container_width=True)

    an3, an4 = st.columns(2)

    with an3:
        # Evacuation capacity
        evac_all = get_evacuation_data()
        fig_cap = go.Figure()
        fig_cap.add_bar(
            name="People Needing Evacuation",
            x=[e["village"] for e in evac_all],
            y=[e["population"] for e in evac_all],
            marker_color="#ef4444"
        )
        fig_cap.add_bar(
            name="Shelter Free Capacity",
            x=[e["village"] for e in evac_all],
            y=[e["shelter_capacity"] - e["shelter_occupancy"] for e in evac_all],
            marker_color="#38a5ff"
        )
        fig_cap.update_layout(
            barmode="group",
            title="Evacuation Need vs Shelter Capacity",
            template="plotly_dark",
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="rgba(255,255,255,0.8)", size=9),
            height=320, xaxis_tickangle=-25,
            legend=dict(bgcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig_cap, use_container_width=True)

    with an4:
        # Resource coverage radar
        rel = get_relief_resources()[0]
        rkeys = ["food_packets", "drinking_water_liters", "medicines_kits", "rescue_teams", "rescue_boats"]
        rlabels = ["Food", "Water", "Medicine", "Rescue\nTeams", "Boats"]
        pcts = [
            round(rel["resources"][rk]["available"] / rel["resources"][rk]["required"] * 100, 1)
            for rk in rkeys
        ]
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=pcts,
            theta=rlabels,
            fill="toself",
            line_color="#38a5ff",
            fillcolor="rgba(56,165,255,0.15)",
            name=rel["location"][:20],
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], color="rgba(255,255,255,0.4)"),
                angularaxis=dict(color="rgba(255,255,255,0.6)"),
                bgcolor="rgba(0,0,0,0)",
            ),
            showlegend=False,
            title=f"Resource Coverage % — {rel['location'][:25]}",
            template="plotly_dark",
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="rgba(255,255,255,0.8)", size=10),
            height=320,
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # Full district table
    st.markdown("---")
    st.markdown('<div class="sec-hdr">📋 Complete Coastal District Risk Table</div>', unsafe_allow_html=True)
    df_full = pd.DataFrame([{
        "District": d["name"],
        "Risk Level": d["risk_level"],
        "Population": d["population"],
        "Pop at Risk": d["pop_at_risk"],
        "Villages at Risk": d["villages_at_risk"],
        "Coastal Length (km)": d["coastal_length_km"],
        "Fishing Zones": ", ".join(d["fishing_zones"]),
    } for d in districts])
    st.dataframe(df_full, use_container_width=True, hide_index=True,
        column_config={
            "Population": st.column_config.NumberColumn("Population", format="%d"),
            "Pop at Risk": st.column_config.NumberColumn("Pop at Risk", format="%d"),
        }
    )


# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────

st.markdown("---")
st.markdown("""
<div style="text-align:center; padding:14px; color:rgba(255,255,255,0.25); font-size:0.75rem; line-height:1.7;">
    🌀 <strong style="color:rgba(255,255,255,0.4);">CoastGuard AI</strong> &nbsp;·&nbsp;
    Smart Cyclone & Coastal Disaster Early Warning System &nbsp;·&nbsp; Gujarat, India &nbsp;·&nbsp;<br>
    Central Agent: <strong style="color:rgba(56,165,255,0.6);">Coastal Disaster Response Agent</strong> &nbsp;·&nbsp;
    Powered by <strong style="color:rgba(56,165,255,0.6);">IBM Granite AI + IBM Cloud + IBM Bob</strong> &nbsp;·&nbsp;
    Hackathon Prototype &nbsp;·&nbsp;
    <strong style="color:rgba(251,191,36,0.6);">⚠️ DEMO DATA — Not for real emergency use</strong>
</div>
""", unsafe_allow_html=True)
