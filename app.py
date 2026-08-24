"""
Gujarat SmartGuide AI — Main Application
==========================================
Run with:  streamlit run app.py
"""

import sys
import os

# Ensure project root is on the path so sub-modules resolve correctly
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from data.data_service import (
    get_all_locations,
    get_districts,
    get_by_district,
    search_locations,
    get_by_name,
    get_top_by_population,
    get_stats,
)
from data.weather_service import get_weather_for_location, describe_weather
from data.charts import (
    get_population_chart_data,
    get_district_count_data,
    get_weather_comparison_data,
)
from agent.chat_engine import chat

# ─────────────────────────────────────────────
# Page Configuration
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Gujarat SmartGuide AI",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Custom CSS — Modern Professional Theme
# ─────────────────────────────────────────────

st.markdown("""
<style>
/* ── Import Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

/* ── Hide default Streamlit branding ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ── Main background ── */
.stApp {
    background: linear-gradient(135deg, #0f1117 0%, #1a1f2e 50%, #0f1117 100%);
    min-height: 100vh;
}

/* ── Top Header Banner ── */
.header-banner {
    background: linear-gradient(135deg, #1e3a5f 0%, #2d5986 40%, #1a4f7a 100%);
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 24px;
    border: 1px solid rgba(99, 172, 229, 0.3);
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    position: relative;
    overflow: hidden;
}
.header-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(99,172,229,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.header-title {
    font-size: 2.2rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0;
    letter-spacing: -0.5px;
}
.header-subtitle {
    font-size: 1rem;
    color: rgba(255,255,255,0.75);
    margin: 6px 0 0 0;
    font-weight: 400;
}
.header-badge {
    display: inline-block;
    background: rgba(255,193,7,0.2);
    color: #ffc107;
    border: 1px solid rgba(255,193,7,0.4);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-top: 10px;
}

/* ── Stat Cards ── */
.stat-card {
    background: linear-gradient(135deg, #1e2535 0%, #252d40 100%);
    border: 1px solid rgba(99,172,229,0.2);
    border-radius: 12px;
    padding: 18px 20px;
    text-align: center;
    transition: transform 0.2s, box-shadow 0.2s;
}
.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 24px rgba(0,0,0,0.3);
}
.stat-number {
    font-size: 1.8rem;
    font-weight: 700;
    color: #63ace5;
    margin: 0;
}
.stat-label {
    font-size: 0.8rem;
    color: rgba(255,255,255,0.55);
    margin: 4px 0 0 0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ── Weather Card ── */
.weather-card {
    background: linear-gradient(135deg, #1a3a5c 0%, #1e4d78 60%, #1a3a5c 100%);
    border: 1px solid rgba(99,172,229,0.35);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.weather-icon {
    font-size: 3rem;
    line-height: 1;
    display: block;
    margin-bottom: 8px;
}
.weather-temp {
    font-size: 2.8rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0;
    line-height: 1;
}
.weather-condition {
    font-size: 1rem;
    color: rgba(255,255,255,0.8);
    margin: 4px 0 16px 0;
}
.weather-location {
    font-size: 1.2rem;
    font-weight: 600;
    color: #63ace5;
    margin: 0 0 4px 0;
}
.weather-detail {
    display: flex;
    justify-content: space-between;
    background: rgba(255,255,255,0.08);
    border-radius: 8px;
    padding: 10px 14px;
    margin-top: 8px;
}
.weather-detail-item {
    text-align: center;
}
.weather-detail-value {
    font-size: 1.1rem;
    font-weight: 600;
    color: #ffffff;
}
.weather-detail-key {
    font-size: 0.7rem;
    color: rgba(255,255,255,0.55);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.weather-demo-badge {
    background: rgba(255,193,7,0.15);
    color: #ffc107;
    border: 1px solid rgba(255,193,7,0.3);
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 12px;
    display: inline-block;
}

/* ── Location Info Card ── */
.location-card {
    background: linear-gradient(135deg, #1e2535 0%, #252d40 100%);
    border: 1px solid rgba(99,172,229,0.2);
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 16px;
}
.location-name {
    font-size: 1.4rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 4px 0;
}
.location-type-badge {
    display: inline-block;
    background: rgba(99,172,229,0.2);
    color: #63ace5;
    border: 1px solid rgba(99,172,229,0.35);
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 12px;
}
.location-meta {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 14px;
}
.meta-item {
    background: rgba(255,255,255,0.05);
    border-radius: 8px;
    padding: 8px 12px;
}
.meta-key {
    font-size: 0.7rem;
    color: rgba(255,255,255,0.5);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 2px;
}
.meta-value {
    font-size: 0.92rem;
    font-weight: 600;
    color: rgba(255,255,255,0.9);
}
.location-desc {
    font-size: 0.9rem;
    color: rgba(255,255,255,0.75);
    line-height: 1.6;
    margin-bottom: 12px;
}
.key-fact {
    background: rgba(99,172,229,0.08);
    border-left: 3px solid #63ace5;
    border-radius: 0 6px 6px 0;
    padding: 5px 10px;
    font-size: 0.83rem;
    color: rgba(255,255,255,0.8);
    margin-bottom: 5px;
}

/* ── Chat UI ── */
.chat-container {
    background: #1a1f2e;
    border: 1px solid rgba(99,172,229,0.2);
    border-radius: 16px;
    padding: 20px;
    max-height: 500px;
    overflow-y: auto;
}
.chat-message-user {
    background: linear-gradient(135deg, #1e3a5f, #2d5986);
    border: 1px solid rgba(99,172,229,0.3);
    border-radius: 16px 16px 4px 16px;
    padding: 12px 16px;
    margin: 8px 0;
    margin-left: 15%;
    color: #ffffff;
    font-size: 0.92rem;
    line-height: 1.5;
}
.chat-message-ai {
    background: #252d40;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px 16px 16px 4px;
    padding: 12px 16px;
    margin: 8px 0;
    margin-right: 10%;
    color: rgba(255,255,255,0.9);
    font-size: 0.92rem;
    line-height: 1.6;
}
.chat-avatar-ai {
    font-size: 1.3rem;
    margin-bottom: 4px;
}
.chat-label-user {
    font-size: 0.72rem;
    color: rgba(255,255,255,0.5);
    text-align: right;
    margin-bottom: 4px;
}
.chat-label-ai {
    font-size: 0.72rem;
    color: #63ace5;
    margin-bottom: 4px;
    font-weight: 600;
}

/* ── Section Headers ── */
.section-header {
    font-size: 1.05rem;
    font-weight: 700;
    color: rgba(255,255,255,0.9);
    margin: 0 0 14px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(99,172,229,0.2);
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── Search Results ── */
.search-result-item {
    background: #252d40;
    border: 1px solid rgba(99,172,229,0.15);
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 8px;
    cursor: pointer;
    transition: border-color 0.2s, background 0.2s;
}
.search-result-item:hover {
    border-color: rgba(99,172,229,0.45);
    background: #2a334a;
}
.search-result-name {
    font-size: 1rem;
    font-weight: 600;
    color: #ffffff;
}
.search-result-meta {
    font-size: 0.8rem;
    color: rgba(255,255,255,0.55);
    margin-top: 3px;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1322 0%, #141927 100%);
    border-right: 1px solid rgba(99,172,229,0.15);
}
[data-testid="stSidebar"] .stMarkdown {
    color: rgba(255,255,255,0.85);
}

/* ── Streamlit component overrides ── */
.stTextInput > div > div > input {
    background: #252d40 !important;
    border: 1px solid rgba(99,172,229,0.3) !important;
    border-radius: 10px !important;
    color: #ffffff !important;
    font-size: 0.92rem !important;
    padding: 10px 14px !important;
}
.stTextInput > div > div > input:focus {
    border-color: #63ace5 !important;
    box-shadow: 0 0 0 2px rgba(99,172,229,0.15) !important;
}
.stSelectbox > div > div {
    background: #252d40 !important;
    border: 1px solid rgba(99,172,229,0.3) !important;
    border-radius: 10px !important;
    color: #ffffff !important;
}
.stButton > button {
    background: linear-gradient(135deg, #1e3a5f, #2d5986) !important;
    border: 1px solid rgba(99,172,229,0.4) !important;
    border-radius: 10px !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    padding: 8px 20px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2d5986, #3a6fa3) !important;
    border-color: rgba(99,172,229,0.7) !important;
    transform: translateY(-1px) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: rgba(255,255,255,0.6);
    border-radius: 8px 8px 0 0;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    color: #63ace5 !important;
    border-bottom: 2px solid #63ace5 !important;
}
div[data-testid="stMetricValue"] {
    color: #63ace5 !important;
    font-weight: 700 !important;
}

/* ── Info/Warning boxes ── */
.info-box {
    background: rgba(99,172,229,0.1);
    border: 1px solid rgba(99,172,229,0.3);
    border-radius: 10px;
    padding: 12px 16px;
    color: rgba(255,255,255,0.8);
    font-size: 0.88rem;
    margin-bottom: 12px;
}
.demo-warning {
    background: rgba(255,193,7,0.08);
    border: 1px solid rgba(255,193,7,0.25);
    border-radius: 10px;
    padding: 10px 14px;
    color: rgba(255,193,7,0.9);
    font-size: 0.8rem;
    margin-bottom: 12px;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.05); border-radius: 3px; }
::-webkit-scrollbar-thumb { background: rgba(99,172,229,0.4); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(99,172,229,0.7); }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Session State Initialization
# ─────────────────────────────────────────────

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "selected_location" not in st.session_state:
    st.session_state.selected_location = None
if "search_results" not in st.session_state:
    st.session_state.search_results = []
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Dashboard"


# ─────────────────────────────────────────────
# Helper Rendering Functions
# ─────────────────────────────────────────────

def render_weather_card(loc: dict):
    w = loc.get("weather", {})
    from data.weather_service import get_condition_icon
    icon = get_condition_icon(w.get("condition", ""))
    st.markdown(f"""
    <div class="weather-card">
        <div class="weather-location">📍 {loc['name']}, {loc['district']}</div>
        <span class="weather-icon">{icon}</span>
        <div class="weather-temp">{w.get('temperature_c', '--')}°C</div>
        <div class="weather-condition">{w.get('condition', 'N/A')}</div>
        <div class="weather-detail">
            <div class="weather-detail-item">
                <div class="weather-detail-value">💧 {w.get('humidity_percent', '--')}%</div>
                <div class="weather-detail-key">Humidity</div>
            </div>
            <div class="weather-detail-item">
                <div class="weather-detail-value">💨 {w.get('wind_speed_kmh', '--')}</div>
                <div class="weather-detail-key">km/h Wind</div>
            </div>
            <div class="weather-detail-item">
                <div class="weather-detail-value">🌧️ {w.get('rain_chance_percent', '--')}%</div>
                <div class="weather-detail-key">Rain Chance</div>
            </div>
            <div class="weather-detail-item">
                <div class="weather-detail-value">🌡️ {w.get('feels_like_c', '--')}°C</div>
                <div class="weather-detail-key">Feels Like</div>
            </div>
        </div>
        <div class="weather-demo-badge">⚠ Demo Data — Not Real-Time</div>
    </div>
    """, unsafe_allow_html=True)


def render_location_card(loc: dict):
    kf_html = "".join(f'<div class="key-fact">• {f}</div>' for f in loc.get("key_facts", []))
    st.markdown(f"""
    <div class="location-card">
        <div class="location-name">{loc['name']}</div>
        <span class="location-type-badge">{loc['type']}</span>
        <div class="location-meta">
            <div class="meta-item">
                <div class="meta-key">District</div>
                <div class="meta-value">{loc['district']}</div>
            </div>
            <div class="meta-item">
                <div class="meta-key">Population</div>
                <div class="meta-value">{loc['population']:,}</div>
            </div>
            <div class="meta-item">
                <div class="meta-key">Taluka</div>
                <div class="meta-value">{loc.get('taluka', 'N/A')}</div>
            </div>
            <div class="meta-item">
                <div class="meta-key">Area</div>
                <div class="meta-value">{loc.get('area_sq_km', 'N/A')} km²</div>
            </div>
        </div>
        <div class="location-desc">{loc['description']}</div>
        {kf_html}
    </div>
    """, unsafe_allow_html=True)


def render_chat_message(role: str, content: str):
    if role == "user":
        st.markdown(f"""
        <div style="text-align:right">
            <div class="chat-label-user">You</div>
            <div class="chat-message-user">{content}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Convert markdown bold to HTML for display
        import re
        html_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
        html_content = html_content.replace('\n', '<br>')
        # Convert blockquotes
        html_content = re.sub(r'&gt;\s*(.*?)(<br>|$)', r'<em style="color:#63ace5;">\1</em>\2', html_content)
        st.markdown(f"""
        <div>
            <div class="chat-label-ai">🤖 Gujarat SmartGuide AI</div>
            <div class="chat-message-ai">{html_content}</div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 16px 0 24px 0;">
        <div style="font-size:2.5rem;">🏛️</div>
        <div style="font-size:1.1rem; font-weight:700; color:#ffffff; margin-top:8px;">Gujarat SmartGuide AI</div>
        <div style="font-size:0.78rem; color:rgba(255,255,255,0.5); margin-top:4px;">AI-Powered Location Assistant</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div style="font-size:0.8rem; font-weight:600; color:rgba(255,255,255,0.6); text-transform:uppercase; letter-spacing:0.8px; margin-bottom:8px;">Navigation</div>', unsafe_allow_html=True)

    nav_options = ["🏠 Dashboard", "🔍 Search & Explore", "🌤️ Weather", "🤖 AI Chat", "📊 Analytics"]
    nav = st.radio("", nav_options, label_visibility="collapsed")

    st.markdown("---")
    st.markdown("**🗺️ Quick District Filter**")
    districts_list = ["All Districts"] + get_districts()
    selected_district_sidebar = st.selectbox("District", districts_list, label_visibility="collapsed")

    st.markdown("---")
    stats = get_stats()
    st.markdown(f"""
    <div style="font-size:0.78rem; color:rgba(255,255,255,0.5);">
        <div style="margin-bottom:6px;">📍 <strong style="color:#63ace5;">{stats['total_locations']}</strong> locations in dataset</div>
        <div style="margin-bottom:6px;">🗺️ <strong style="color:#63ace5;">{stats['total_districts']}</strong> districts covered</div>
        <div style="margin-bottom:6px;">🏙️ <strong style="color:#63ace5;">{stats['cities']}</strong> cities · <strong style="color:#63ace5;">{stats['towns']}</strong> towns · <strong style="color:#63ace5;">{stats['villages']}</strong> villages</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div class="demo-warning">
        ⚠️ All data shown is <strong>demo/mock data</strong> for educational purposes. Not real-time information.
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────

st.markdown("""
<div class="header-banner">
    <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap;">
        <div>
            <h1 class="header-title">🏛️ Gujarat SmartGuide AI</h1>
            <p class="header-subtitle">AI-Powered Location, Weather & Village Information Assistant for Gujarat</p>
            <span class="header-badge">🎓 College Project · Demo Data</span>
        </div>
        <div style="text-align:right; margin-top:8px;">
            <div style="font-size:0.78rem; color:rgba(255,255,255,0.5);">Kem Cho! 🙏</div>
            <div style="font-size:0.78rem; color:rgba(255,255,255,0.5);">Covering 20 Gujarat Locations</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Top Stats Row
# ─────────────────────────────────────────────

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown(f'<div class="stat-card"><p class="stat-number">{stats["total_locations"]}</p><p class="stat-label">Locations</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="stat-card"><p class="stat-number">{stats["total_districts"]}</p><p class="stat-label">Districts</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="stat-card"><p class="stat-number">{stats["cities"]}</p><p class="stat-label">Cities</p></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="stat-card"><p class="stat-number">{stats["towns"] + stats["villages"]}</p><p class="stat-label">Towns/Villages</p></div>', unsafe_allow_html=True)
with col5:
    total_pop_m = stats["total_population"] / 1_000_000
    st.markdown(f'<div class="stat-card"><p class="stat-number">{total_pop_m:.1f}M</p><p class="stat-label">Total Population</p></div>', unsafe_allow_html=True)

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Main Content — Routed by Sidebar Nav
# ─────────────────────────────────────────────

active_page = nav.split(" ", 1)[1].strip()  # strip emoji

# ══════════════════════════════════════════════
# PAGE: Dashboard
# ══════════════════════════════════════════════
if active_page == "Dashboard":
    left_col, right_col = st.columns([1.2, 1])

    with left_col:
        # ── Quick Search
        st.markdown('<div class="section-header">🔍 Quick Location Search</div>', unsafe_allow_html=True)
        search_input = st.text_input("", placeholder="Search a Gujarat city or village… e.g. Vapi, Surat, Bardoli", key="dash_search", label_visibility="collapsed")

        if search_input:
            results = search_locations(search_input)
            if results:
                st.markdown(f'<div class="info-box">Found <strong>{len(results)}</strong> matching location(s) for "<strong>{search_input}</strong>"</div>', unsafe_allow_html=True)
                for r in results[:4]:
                    btn_label = f"📍 {r['name']} · {r['district']} · Pop: {r['population']:,}"
                    if st.button(btn_label, key=f"dash_btn_{r['id']}"):
                        st.session_state.selected_location = r
            else:
                st.markdown(f'<div class="demo-warning">No results found for "<strong>{search_input}</strong>". Try: Vapi, Surat, Ahmedabad, Bharuch…</div>', unsafe_allow_html=True)

        # ── Selected Location Info
        if st.session_state.selected_location:
            loc = st.session_state.selected_location
            st.markdown('<div class="section-header" style="margin-top:20px;">📍 Location Details</div>', unsafe_allow_html=True)
            render_location_card(loc)

            # Inline weather for selected location
            st.markdown('<div class="section-header">🌤️ Weather (Demo Data)</div>', unsafe_allow_html=True)
            render_weather_card(loc)

            if st.button("✖ Clear Selection", key="clear_sel"):
                st.session_state.selected_location = None
                st.rerun()

        else:
            # Default: show top 3 popular locations
            st.markdown('<div class="section-header" style="margin-top:20px;">🏙️ Featured Locations</div>', unsafe_allow_html=True)
            top3 = get_top_by_population(3)
            for loc in top3:
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.markdown(f"""
                    <div class="search-result-item">
                        <div class="search-result-name">📍 {loc['name']}</div>
                        <div class="search-result-meta">{loc['district']} · {loc['type'].title()} · Pop: {loc['population']:,}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_b:
                    if st.button("View", key=f"top_btn_{loc['id']}"):
                        st.session_state.selected_location = loc
                        st.rerun()

    with right_col:
        # ── District Filter
        st.markdown('<div class="section-header">🗺️ Browse by District</div>', unsafe_allow_html=True)
        district_options = ["Select a district…"] + get_districts()
        chosen_district = st.selectbox("", district_options, key="dist_filter", label_visibility="collapsed")

        if chosen_district != "Select a district…":
            dist_locs = get_by_district(chosen_district)
            st.markdown(f'<div class="info-box">🗺️ <strong>{chosen_district} District</strong> — {len(dist_locs)} location(s)</div>', unsafe_allow_html=True)
            for dl in dist_locs:
                col_x, col_y = st.columns([3, 1])
                with col_x:
                    w_icon = dl.get("weather", {}).get("icon", "🌡️")
                    st.markdown(f"""
                    <div class="search-result-item">
                        <div class="search-result-name">{w_icon} {dl['name']}</div>
                        <div class="search-result-meta">{dl['type'].title()} · Pop: {dl['population']:,} · {dl['weather']['condition']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_y:
                    if st.button("Info", key=f"dist_info_{dl['id']}"):
                        st.session_state.selected_location = dl
                        st.rerun()

        # ── Quick Weather Grid
        st.markdown('<div class="section-header" style="margin-top:20px;">🌡️ Quick Weather Overview</div>', unsafe_allow_html=True)
        top_locs = get_top_by_population(6)
        for i in range(0, len(top_locs), 2):
            c1, c2 = st.columns(2)
            for j, col in enumerate([c1, c2]):
                if i + j < len(top_locs):
                    l = top_locs[i + j]
                    w = l.get("weather", {})
                    from data.weather_service import get_condition_icon
                    ic = get_condition_icon(w.get("condition", ""))
                    with col:
                        st.markdown(f"""
                        <div class="stat-card" style="text-align:left; padding:12px 14px; margin-bottom:8px;">
                            <div style="font-size:0.85rem; font-weight:600; color:#fff;">{ic} {l['name']}</div>
                            <div style="font-size:1.3rem; font-weight:700; color:#63ace5;">{w.get('temperature_c','--')}°C</div>
                            <div style="font-size:0.72rem; color:rgba(255,255,255,0.5);">{w.get('condition','')}</div>
                        </div>
                        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════
# PAGE: Search & Explore
# ══════════════════════════════════════════════
elif active_page == "Search & Explore":
    st.markdown('<div class="section-header">🔍 Search & Explore Gujarat Locations</div>', unsafe_allow_html=True)

    search_col, filter_col = st.columns([2, 1])
    with search_col:
        search_q = st.text_input("", placeholder="Type a location name, district, or keyword…", key="explore_search", label_visibility="collapsed")
    with filter_col:
        type_filter = st.selectbox("", ["All Types", "City", "Town", "Village"], key="type_filter", label_visibility="collapsed")

    # Build full list with optional filters
    if search_q:
        all_results = search_locations(search_q)
    elif selected_district_sidebar != "All Districts":
        all_results = get_by_district(selected_district_sidebar)
    else:
        all_results = get_all_locations()

    if type_filter != "All Types":
        all_results = [r for r in all_results if r["type"].lower() == type_filter.lower()]

    st.markdown(f'<div class="info-box">Showing <strong>{len(all_results)}</strong> location(s)</div>', unsafe_allow_html=True)

    if all_results:
        # Create a DataFrame for display
        df_data = []
        for r in all_results:
            df_data.append({
                "Name": r["name"],
                "District": r["district"],
                "Type": r["type"].title(),
                "Population": r["population"],
                "Weather": r.get("weather", {}).get("condition", "N/A"),
                "Temp (°C)": r.get("weather", {}).get("temperature_c", "N/A"),
            })
        df = pd.DataFrame(df_data)

        # Color-coded table
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Population": st.column_config.NumberColumn("Population", format="%d"),
                "Temp (°C)": st.column_config.NumberColumn("Temp (°C)", format="%d°C"),
            }
        )

        # Detail view
        st.markdown("---")
        st.markdown('<div class="section-header">📋 Location Details</div>', unsafe_allow_html=True)
        names = [r["name"] for r in all_results]
        selected_name = st.selectbox("Select a location to view details:", names, key="detail_select")
        if selected_name:
            loc = get_by_name(selected_name)
            if loc:
                dc1, dc2 = st.columns(2)
                with dc1:
                    render_location_card(loc)
                with dc2:
                    render_weather_card(loc)


# ══════════════════════════════════════════════
# PAGE: Weather
# ══════════════════════════════════════════════
elif active_page == "Weather":
    st.markdown('<div class="section-header">🌤️ Gujarat Weather Dashboard (Demo Data)</div>', unsafe_allow_html=True)
    st.markdown('<div class="demo-warning">⚠️ All weather data displayed here is <strong>demo/mock data</strong>. It is not real-time or live weather. See weather_service.py to connect a real API.</div>', unsafe_allow_html=True)

    # Location selector
    all_locs = get_all_locations()
    loc_names = [l["name"] for l in all_locs]
    selected_w_name = st.selectbox("Select a location:", loc_names, key="weather_select")

    if selected_w_name:
        loc = get_by_name(selected_w_name)
        if loc:
            wc1, wc2 = st.columns([1, 1])
            with wc1:
                render_weather_card(loc)
            with wc2:
                st.markdown('<div class="section-header">📍 Location Overview</div>', unsafe_allow_html=True)
                w = loc.get("weather", {})
                st.markdown(f"""
                <div class="location-card">
                    <div class="location-name">{loc['name']}</div>
                    <span class="location-type-badge">{loc['type']}</span>
                    <div class="location-meta">
                        <div class="meta-item"><div class="meta-key">District</div><div class="meta-value">{loc['district']}</div></div>
                        <div class="meta-item"><div class="meta-key">Population</div><div class="meta-value">{loc['population']:,}</div></div>
                    </div>
                    <div class="location-desc" style="font-size:0.85rem;">{loc['description'][:200]}…</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")
    # Temperature comparison chart
    st.markdown('<div class="section-header">🌡️ Temperature Comparison Across Locations</div>', unsafe_allow_html=True)
    wdata = get_weather_comparison_data()
    df_w = pd.DataFrame({
        "Location": wdata["names"],
        "Temperature (°C)": wdata["temperatures"],
        "Humidity (%)": wdata["humidity"],
        "Rain Chance (%)": wdata["rain_chance"],
    })

    chart_tab1, chart_tab2, chart_tab3 = st.tabs(["🌡️ Temperature", "💧 Humidity", "🌧️ Rain Chance"])
    with chart_tab1:
        fig_temp = px.bar(
            df_w, x="Location", y="Temperature (°C)",
            color="Temperature (°C)",
            color_continuous_scale=["#1a6b8a", "#e07b39", "#c62828"],
            title="Demo Temperature by Location (°C)",
            template="plotly_dark",
        )
        fig_temp.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="rgba(255,255,255,0.8)"),
            showlegend=False, coloraxis_showscale=False,
        )
        st.plotly_chart(fig_temp, use_container_width=True)
    with chart_tab2:
        fig_hum = px.bar(
            df_w, x="Location", y="Humidity (%)",
            color="Humidity (%)",
            color_continuous_scale=["#1e5f74", "#63ace5"],
            title="Demo Humidity by Location (%)",
            template="plotly_dark",
        )
        fig_hum.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="rgba(255,255,255,0.8)"), showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig_hum, use_container_width=True)
    with chart_tab3:
        fig_rain = px.bar(
            df_w, x="Location", y="Rain Chance (%)",
            color="Rain Chance (%)",
            color_continuous_scale=["#2e7d32", "#00bcd4"],
            title="Demo Rain Chance by Location (%)",
            template="plotly_dark",
        )
        fig_rain.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="rgba(255,255,255,0.8)"), showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig_rain, use_container_width=True)


# ══════════════════════════════════════════════
# PAGE: AI Chat
# ══════════════════════════════════════════════
elif active_page == "AI Chat":
    st.markdown('<div class="section-header">🤖 AI Chat Assistant</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        Ask me anything about Gujarat locations, weather, population, districts, and more.
        I answer using the local demo dataset — no internet required.
    </div>
    """, unsafe_allow_html=True)

    chat_main, chat_side = st.columns([2, 1])

    with chat_main:
        # Display chat history
        if not st.session_state.chat_history:
            # Welcome message
            welcome = chat("hello")
            st.session_state.chat_history.append({"role": "assistant", "content": welcome})

        for msg in st.session_state.chat_history:
            render_chat_message(msg["role"], msg["content"])

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        # Input
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input("", placeholder="Ask about Gujarat… e.g. What is the weather in Vapi?", key="chat_input", label_visibility="collapsed")
            col_send, col_clear = st.columns([3, 1])
            with col_send:
                send = st.form_submit_button("📤 Send", use_container_width=True)
            with col_clear:
                clear = st.form_submit_button("🗑️ Clear", use_container_width=True)

        if send and user_input.strip():
            user_msg = user_input.strip()
            st.session_state.chat_history.append({"role": "user", "content": user_msg})
            ai_response = chat(user_msg)
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            st.rerun()

        if clear:
            st.session_state.chat_history = []
            st.rerun()

    with chat_side:
        st.markdown('<div class="section-header">💡 Try Asking</div>', unsafe_allow_html=True)
        sample_questions = [
            "What is the weather in Vapi?",
            "Tell me about Surat",
            "Which city has the highest population?",
            "Show locations in Valsad",
            "What is Bharuch known for?",
            "Weather in Ahmedabad?",
            "Which district does Bardoli belong to?",
            "Tell me about Navsari",
            "Show me villages in Valsad",
            "Population of Vadodara",
        ]
        for q in sample_questions:
            if st.button(f"💬 {q}", key=f"sample_{q[:20]}", use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": q})
                ai_response = chat(q)
                st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
                st.rerun()

        st.markdown("---")
        st.markdown("""
        <div class="demo-warning">
            🤖 This AI uses local rule-based matching — no external API required.
            For OpenAI/LangChain support, see <code>agent/chat_engine.py</code>.
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# PAGE: Analytics
# ══════════════════════════════════════════════
elif active_page == "Analytics":
    st.markdown('<div class="section-header">📊 Gujarat Data Analytics (Demo Dataset)</div>', unsafe_allow_html=True)
    st.markdown('<div class="demo-warning">⚠️ All figures are from demo/mock data for educational purposes only.</div>', unsafe_allow_html=True)

    # ── Population Chart
    pop_data = get_population_chart_data()
    df_pop = pd.DataFrame({
        "Location": pop_data["names"],
        "Population": pop_data["populations"],
        "District": pop_data["districts"],
        "Type": pop_data["types"],
    })

    st.markdown('<div class="section-header">👥 Population by Location</div>', unsafe_allow_html=True)
    fig_pop = px.bar(
        df_pop, x="Location", y="Population",
        color="District",
        title="Population Distribution Across Gujarat Demo Locations",
        template="plotly_dark",
        text="Population",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig_pop.update_traces(texttemplate='%{text:,}', textposition='outside', textfont_size=9)
    fig_pop.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="rgba(255,255,255,0.8)"),
        xaxis_tickangle=-45,
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(255,255,255,0.1)"),
        height=450,
    )
    st.plotly_chart(fig_pop, use_container_width=True)

    # ── District breakdown + Pie chart
    dist_data = get_district_count_data()
    an1, an2 = st.columns(2)

    with an1:
        st.markdown('<div class="section-header">🗺️ Locations per District</div>', unsafe_allow_html=True)
        fig_dist = px.bar(
            x=dist_data["districts"], y=dist_data["counts"],
            labels={"x": "District", "y": "Locations"},
            color=dist_data["counts"],
            color_continuous_scale=["#1a4f7a", "#63ace5"],
            template="plotly_dark",
            title="Number of Locations per District",
        )
        fig_dist.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="rgba(255,255,255,0.8)"),
            coloraxis_showscale=False,
            showlegend=False,
        )
        st.plotly_chart(fig_dist, use_container_width=True)

    with an2:
        st.markdown('<div class="section-header">🥧 Population Share by District</div>', unsafe_allow_html=True)
        all_locs = get_all_locations()
        dist_pop: dict[str, int] = {}
        for l in all_locs:
            dist_pop[l["district"]] = dist_pop.get(l["district"], 0) + l["population"]

        fig_pie = px.pie(
            names=list(dist_pop.keys()),
            values=list(dist_pop.values()),
            title="Population Share by District (Demo Data)",
            template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig_pie.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="rgba(255,255,255,0.8)"),
            legend=dict(bgcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # ── Type Breakdown
    st.markdown('<div class="section-header">🏙️ Location Type Breakdown</div>', unsafe_allow_html=True)
    type_counts = {"Cities": stats["cities"], "Towns": stats["towns"], "Villages": stats["villages"]}
    fig_type = px.pie(
        names=list(type_counts.keys()),
        values=list(type_counts.values()),
        title="Location Types in Dataset",
        template="plotly_dark",
        color_discrete_map={"Cities": "#63ace5", "Towns": "#7c5cd8", "Villages": "#43b581"},
        hole=0.4,
    )
    fig_type.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="rgba(255,255,255,0.8)"))
    st.plotly_chart(fig_type, use_container_width=True)

    # ── Full data table
    st.markdown("---")
    st.markdown('<div class="section-header">📋 Full Location Dataset</div>', unsafe_allow_html=True)
    full_df_data = []
    for l in get_all_locations():
        full_df_data.append({
            "Name": l["name"],
            "Type": l["type"].title(),
            "District": l["district"],
            "Taluka": l.get("taluka", ""),
            "Population": l["population"],
            "Area (km²)": l.get("area_sq_km", ""),
            "Nearby City": l.get("nearby_city", ""),
            "Weather Condition": l["weather"]["condition"],
            "Temp (°C)": l["weather"]["temperature_c"],
            "Humidity (%)": l["weather"]["humidity_percent"],
        })
    full_df = pd.DataFrame(full_df_data)
    st.dataframe(full_df, use_container_width=True, hide_index=True,
        column_config={
            "Population": st.column_config.NumberColumn("Population", format="%d"),
        }
    )


# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────

st.markdown("---")
st.markdown("""
<div style="text-align:center; padding: 16px; color: rgba(255,255,255,0.35); font-size: 0.8rem;">
    🏛️ <strong style="color:rgba(255,255,255,0.5);">Gujarat SmartGuide AI</strong> &nbsp;·&nbsp; College Project &nbsp;·&nbsp; Demo Data Only &nbsp;·&nbsp; Not affiliated with any government body &nbsp;·&nbsp;
    Built with Streamlit + Plotly
</div>
""", unsafe_allow_html=True)
