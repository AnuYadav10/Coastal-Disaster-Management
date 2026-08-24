# 🏛️ Gujarat SmartGuide AI

> **AI-Powered Location, Weather & Village Information Assistant for Gujarat**
> College Project · Demo Data · Built with Streamlit

---

## 📋 Project Overview

Gujarat SmartGuide AI is a professional, interactive web application that serves as an AI assistant for Gujarat, India. It helps users discover information about cities, towns, and villages across Gujarat — including weather conditions, population statistics, district details, and geographic information.

All data is clearly labeled **demo/mock data** for educational purposes.

---

## 🗂️ Project Structure

```
Coastal_Disaster_AI/
├── app.py                        # Main Streamlit application (entry point)
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variable template
│
├── agent/
│   ├── __init__.py
│   └── chat_engine.py            # AI chat assistant (rule-based NLP engine)
│
├── data/
│   ├── __init__.py
│   ├── gujarat_locations.json    # Demo dataset — 20 Gujarat locations
│   ├── data_service.py           # Data loading, querying, filtering
│   ├── weather_service.py        # Weather data + API integration point
│   └── charts.py                 # Chart data preparation
│
└── ui/                           # (Reserved for future component files)
```

---

## 🚀 How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch the application
```bash
streamlit run app.py
```

The app opens at **http://localhost:8501** in your browser.

No API keys are required. Everything works offline using the local demo dataset.

---

## 🤖 How the AI Assistant Works

The chat engine (`agent/chat_engine.py`) uses **rule-based intent detection**:

1. **Intent Classification** — Regex patterns detect query type (weather, population, district, list, info, greeting, help)
2. **Location Extraction** — Scans query text for Gujarat location names from the dataset, then falls back to preposition-based extraction ("weather in **X**")
3. **Data Lookup** — Routes to the appropriate `data_service.py` function
4. **Response Formatting** — Returns a structured Markdown response

No external LLM or API is required for this core functionality. This makes the application:
- Fast and reliable
- Fully offline capable
- Easy to understand and extend

---

## 📊 How Mock Data Works

All location and weather data lives in `data/gujarat_locations.json`.

Each entry contains:
- Basic info: name, type, district, population, taluka, area, description
- Key facts (bullet points)
- Weather snapshot: temperature, humidity, wind, rain chance, condition

The `data_service.py` module loads this JSON at startup and caches it in memory. All search, filter, and AI responses draw from this cached data.

**To modify the data:** Edit `data/gujarat_locations.json` directly. Add new location objects following the existing schema. The application will pick them up automatically on restart.

---

## 🌤️ How to Connect a Real Weather API

Currently, weather data comes from the embedded JSON file. To use live weather:

**Option A — OpenWeatherMap (free tier):**
1. Sign up at https://openweathermap.org/api
2. Copy your API key to `.env` file: `WEATHER_API_KEY=your_key`
3. In `data/weather_service.py`, replace the `get_weather_for_location()` function body with the API call documented in the module's docstring

**Option B — WeatherAPI.com (free tier):**
1. Sign up at https://www.weatherapi.com
2. Same process — the endpoint URL differs (documented in `weather_service.py`)

The rest of the application does **not** need changes — it calls `get_weather_for_location()` regardless of the source.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| **Python 3.11+** | Core language |
| **Streamlit 1.45** | Web UI framework |
| **Plotly 5.x** | Interactive charts |
| **Pandas** | Data manipulation / table display |
| **LangChain / OpenAI** | Optional advanced LLM chat (future) |
| **python-dotenv** | Environment variable management |

---

## 📍 Dataset Coverage

| District | Locations |
|---|---|
| Valsad | Vapi, Valsad, Udvada, Bulsar, Umbergaon, Pardi |
| Surat | Surat, Bardoli |
| Navsari | Navsari, Gandevi, Chikhli |
| Bharuch | Bharuch, Ankleshwar |
| Ahmedabad | Ahmedabad |
| Gandhinagar | Gandhinagar |
| Vadodara | Vadodara |
| Panchmahal | Halol |
| Rajkot | Rajkot |
| Jamnagar | Jamnagar |
| Bhavnagar | Bhavnagar |

---

## ⚠️ Important Disclaimer

All data in this project is **demo/mock data** created for educational and demonstration purposes only. It is:
- Not real-time
- Not affiliated with any government or official body
- Not guaranteed to be accurate
- Intended solely for a college project demonstration

---

## 📱 Application Pages

| Page | Description |
|---|---|
| **Dashboard** | Overview, quick search, district filter, weather grid |
| **Search & Explore** | Full searchable/filterable location table with details |
| **Weather** | Weather dashboard with comparison charts |
| **AI Chat** | Conversational assistant for Gujarat queries |
| **Analytics** | Population charts, district breakdown, pie charts |

---

*Made with ❤️ as a college AI project. Gujarat SmartGuide AI.*
