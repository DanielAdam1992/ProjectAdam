import streamlit as st
from datetime import datetime, timedelta, timezone
import pytz
import requests
import folium
from streamlit_folium import folium_static
from tzlocal import get_localzone_name

# API
API_KEY_WEATHER = "67c4244714a6b3622cd4844889e9728c"
API_KEY_TRIP    = "5ae2e3f221c38a28845f05b6072cf50482464e992930cf2"

def fetch_json(url, params):
    """Safe GET returning JSON or {}."""
    try:
        r = requests.get(url, params=params)
        r.raise_for_status()
        return r.json()
    except:
        return {}

def get_weather(city):
    return fetch_json(
        "https://api.openweathermap.org/data/2.5/weather",
        {"q": city, "appid": API_KEY_WEATHER}
    )

def get_population(city):
    data = fetch_json(
        "https://api.opentripmap.com/0.1/en/places/geoname",
        {"name": city, "apikey": API_KEY_TRIP}
    )
    return data.get("population", "Unknown")

def get_city_time(offset_sec: int) -> datetime:
    """Convert UTC now to local city time given offset seconds."""
    tz = timezone(timedelta(seconds=offset_sec))
    return datetime.now(timezone.utc).astimezone(tz)

# — Streamlit UI setup —
st.set_page_config(page_title="Weather & Time App", layout="wide")
st.title("🌞 Weather & Time Explorer 🌧️")

# — Show user’s local time —
user_tz = get_localzone_name()
user_now = datetime.now(pytz.timezone(user_tz))
st.markdown(f"**Your local time ({user_tz}):**  {user_now.strftime('%A, %B %d, %Y — %I:%M %p')}")


with st.form("input_form", clear_on_submit=False):
    name = st.text_input("Enter your name")
    city = st.text_input("Enter city to lookup", "London")
    submitted = st.form_submit_button("Check Weather 🔎")

if not submitted:
    st.info("Fill out the form above and click **Check Weather 🔎**")
    st.stop()


weather = get_weather(city)
if not weather or "main" not in weather:
    st.error(f"❌ Could not fetch weather for '{city}'.")
    st.stop()

temp_c    = weather["main"]["temp"] - 273.15
humidity  = weather["main"]["humidity"]
clouds    = weather["clouds"]["all"]
icon      = weather["weather"][0]["icon"]
desc      = weather["weather"][0]["description"].title()
tz_offset = weather.get("timezone", 0)
lat, lon  = weather["coord"]["lat"], weather["coord"]["lon"]

city_now  = get_city_time(tz_offset)
local_now = datetime.now()


if name:
    st.subheader(f"Hello {name}! Here's the latest for **{city.title()}**:")

col1, col2, col3, col4 = st.columns([1,1,1,1], gap="small")
col1.metric("🌡 Temperature", f"{temp_c:.1f} °C")
col2.metric("💧 Humidity", f"{humidity}%")
col3.metric("☁️ Cloud Cover", f"{clouds}%")
col4.image(f"https://openweathermap.org/img/wn/{icon}@2x.png", width=64, caption=desc)

st.markdown("---")
t1, t2 = st.columns(2, gap="medium")
t1.write(f"**🕒 Your Local Time:**  {local_now.strftime('%A, %B %d, %Y — %I:%M %p')}")
t2.write(f"**🕒 Time in {city.title()}:**  {city_now.strftime('%A, %B %d, %Y — %I:%M %p')}")

st.markdown("---")
population = get_population(city)
st.write(f"**👥 Population of {city.title()}:** {population}")


st.markdown("---")
with st.expander("Show Location on Map"):
    m = folium.Map(location=[lat, lon], zoom_start=10)
    folium.Marker([lat, lon], popup=city.title()).add_to(m)
    folium_static(m)
