import streamlit as st
from datetime import datetime
import pytz
import requests
import folium
from streamlit_folium import folium_static

# API key to openweathermap with geolocation
API_KEY_WEATHER = "67c4244714a6b3622cd4844889e9728c"
# API key to opentripmap
API_KEY_TRIP = "5ae2e3f221c38a28845f05b6072cf50482464e992930cf4c2ace5cf2"
resp = requests.get("https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY_WEATHER}")


st.title('🌞 Weather App 🌧️')

name = st.text_input('Enter your name', '')
# Entering User Name for greetings
if name:
    st.write(f'Hello {name}, nice weather we having?')
# Telling user the weather and population based on location he chooses

city = st.text_input('Enter the city you heading to: ', 'London')

# getting local and city times


if city:
    st.button('Check Weather 🔎')
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY_WEATHER}'
    rest_weather = requests.get(weather_url)
    data_weather = rest_weather.json()
    state_url =f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={API_KEY_WEATHER}"
    rest_state = requests.get(state_url)
    data_state = rest_state.json()


    if rest_weather.status_code == 200 and 'main' in data_weather:
        temp = data_weather['main']['temp'] - 273.15
        humidity = data_weather['main']['humidity']
        cloud = data_weather['clouds']['all']
        lon = data_weather['coord']['lon']
        lat = data_weather['coord']['lat']

        st.write(f"* The weather in {city} is **{temp:.2f}°** with **{humidity}%** humidity. **{cloud}%** of the sky covered with clouds.  " )

        trip_url = f"https://api.opentripmap.com/0.1/en/places/geoname?name={city}&apikey={API_KEY_TRIP}"

        rest_trip = requests.get(trip_url)
        data_trip = rest_trip.json()
        population = data_trip.get("population", "Unknown")

        st.write(f"* Did you know that the population of {city} is **{population}**.")

        # showing image of the weather in the city the user chose
        weather_main = data_weather['weather'][0]['main']

        weather_images = {
            'Clear': 'https://openweathermap.org/img/wn/01d@2x.png',
            'Clouds': 'https://openweathermap.org/img/wn/03d@2x.png',
            'Rain': 'https://openweathermap.org/img/wn/09d@2x.png',
            'Thunderstorm': 'https://openweathermap.org/img/wn/11d@2x.png',
            'Snow': 'https://openweathermap.org/img/wn/13d@2x.png',
            'Mist': 'https://openweathermap.org/img/wn/50d@2x.png',
        }

        image_url = weather_images.get(weather_main, 'https://openweathermap.org/img/wn/01d@2x.png')
        st.image(image_url, caption=f"**Current weather: {weather_main}**", width=100)
        #showing map
        m = folium.Map(location=[lat, lon], zoom_start=10)
        folium.Marker([lat, lon], popup="Requested Location").add_to(m)
        st_data = folium_static(m)
    else:
        message = data_weather.get('message', 'City not found.')
        st.warning(f"Could not fetch weather data for '{city}'. Reason: {message}")



