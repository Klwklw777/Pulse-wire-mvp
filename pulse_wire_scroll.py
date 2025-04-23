import streamlit as st
import requests

# --- API CONFIG ---
API_KEY = "9247ae535ae7f3fac2ab070f0a839ff9"
DEFAULT_CITY = "Lexington"

# --- FUNCTION TO FETCH WEATHER DATA ---
def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        return {
            "temp": data["main"]["temp"],
            "pressure": data["main"]["pressure"],
            "humidity": data["main"]["humidity"],
            "rain": data.get("rain", {}).get("1h", 0.0),
        }
    else:
        return None

# --- EBRIL LOGIC FOR SCROLLS ---
def generate_scroll(temp, pressure, rain):
    if rain > 1.5 or temp < 8 or pressure < 1000:
        return "Override", "Too much rain or unstable pressure"
    elif 8 <= temp <= 24 and 1000 <= pressure <= 1020 and rain < 1.0:
        return "Flow", "Conditions aligned: temperature, pressure, and rainfall are in rhythm"
    elif 24 < temp < 28 and pressure > 1020:
        return "Reclaim", "Warming trend and stable pressure returning"
    else:
        return "Hesitation", "Signal fluctuations—no clear alignment yet"

# --- STREAMLIT UI ---
st.title("Pulse Wire OS – Land Readiness Scroll")

city = st.text_input("Enter a location (e.g., Lexington):", DEFAULT_CITY)

if st.button("Generate Scroll"):
    data = get_weather_data(city)
    if data:
        scroll, reason = generate_scroll(data["temp"], data["pressure"], data["rain"])
        st.subheader(f"Scroll: {scroll}")
        st.markdown(f"**Reason:** {reason}")
        st.markdown("---")
        st.json(data)
    else:
        st.error("Could not fetch weather data. Try a different city.")

st.markdown("---")
st.header("USDA Crop Condition Scroll")

usda_api_key ="C48C82EB-E034-3E6B-AD43-1E8F58E74CE5"

params = {
    'key': usda_api_key,
    'commodity_desc': 'CORN',
    'statisticcat_desc': 'CONDITION',
    'year': '2024',
    'state_alpha': 'KY',
    'format': 'JSON'
}

if st.button("Generate Crop Scroll"):
    response = requests.get('https://quickstats.nass.usda.gov/api/api_GET/', params=params)
    if response.status_code == 200:
        data = response.json()
        corn_condition = data["data"]
        if corn_condition:
            recent = corn_condition[0]
            condition = recent["Value"]
            scroll = "Flow" if "Good" in condition or "Excellent" in condition else "Override"
            st.subheader(f"Scroll: {scroll}")
            st.markdown(f"**Crop Condition:** {recent['short_desc']} = {condition}")
        else:
            st.warning("No crop condition data available for this year.")
    else:
        st.error("Failed to fetch USDA data.")

st.markdown("---")
st.header("Rytha OS – Overall Readiness Scroll")

# Capture individual scrolls (these would be set when other modules run)

# Dynamically retrieve latest scroll states from session
weather_scroll = st.session_state.get("weather_scroll", "Hesitation")
usda_scroll = st.session_state.get("usda_scroll", "Hesitation")
market_scroll = st.session_state.get("market_scroll", "Hesitation")

scrolls = [weather_scroll, usda_scroll, market_scroll]

st.markdown("---")
st.header("Corn Market Scroll – Futures Rhythm")

prev_corn = st.number_input("Previous Corn Futures Price ($/bushel)", step=0.01, key="prev_corn")
curr_corn = st.number_input("Current Corn Futures Price ($/bushel)", step=0.01, key="curr_corn")

def corn_scroll_logic(prev, curr):
    if prev == 0:
        return "Hesitation", "No baseline price provided"
    
    diff = curr - prev
    pct_change = abs(diff / prev) * 100

    if pct_change > 4:
        return "Override", f"Volatility spike: {pct_change:.2f}% change"
    elif 2 <= pct_change <= 4:
        return "Reclaim", f"Market rebounding or correcting ({pct_change:.2f}% change)"
    elif pct_change < 2:
        return "Flow", f"Stable rhythm in corn market ({pct_change:.2f}% change)"
    else:
        return "Hesitation", "Unable to detect scroll clarity"

if st.button("Generate Corn Scroll"):
    if prev_corn > 0 and curr_corn > 0:
        scroll, reason = corn_scroll_logic(prev_corn, curr_corn)
        st.subheader(f"Corn Scroll: {scroll}")
        st.markdown(f"**Reason:** {reason}")

st.markdown("---")
st.header("Gold Market Scroll – Macro Economic Rhythm")

prev_gold = st.number_input("Previous Gold Price ($/oz)", step=0.01, key="prev_gold")
curr_gold = st.number_input("Current Gold Price ($/oz)", step=0.01, key="curr_gold")

def gold_scroll_logic(prev, curr):
    if prev == 0:
        return "Hesitation", "No baseline price provided"
    
    diff = curr - prev
    pct_change = abs(diff / prev) * 100

    if pct_change > 3:
        return "Override", f"Gold price spiked ({pct_change:.2f}%) – economic volatility"
    elif 1 <= pct_change <= 3:
        return "Reclaim", f"Gold adjusting or stabilizing ({pct_change:.2f}%)"
    elif pct_change < 1:
        return "Flow", f"Stable rhythm in gold market ({pct_change:.2f}%)"
    else:
        return "Hesitation", "No clear scroll condition"

if st.button("Generate Gold Scroll"):
    if prev_gold > 0 and curr_gold > 0:
        scroll, reason = gold_scroll_logic(prev_gold, curr_gold)
        st.session_state["gold_scroll"] = scroll
        st.subheader(f"Gold Scroll: {scroll}")
        st.markdown(f"**Reason:** {reason}")


# Get latest gold scroll value from session
gold_scroll = st.session_state.get("gold_scroll", "Hesitation")

# Final scroll pool that includes all domains
scrolls = [weather_scroll, usda_scroll, market_scroll, gold_scroll]


def overall_scroll(scrolls):
    flow_count = scrolls.count("Flow")
    reclaim_count = scrolls.count("Reclaim")
    override_count = scrolls.count("Override")
    hesitation_count = scrolls.count("Hesitation")

    if override_count >= 2:
        return "Override", "Multiple systems are misaligned"
    elif reclaim_count >= 2:
        return "Reclaim", "Systems recovering from override"
    elif flow_count >= 3:
        return "Flow", "All key systems in rhythm"
    elif hesitation_count >= 2:
        return "Hesitation", "Lack of signal clarity across systems"
    else:
        return "Hesitation", "Mixed rhythm states detected"

if st.button("Generate Overall Rytha Scroll"):
    scroll, reason = overall_scroll(scrolls)
    st.subheader(f"Overall Scroll: {scroll}")
    st.markdown(f"**Reason:** {reason}")

