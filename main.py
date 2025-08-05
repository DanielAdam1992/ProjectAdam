import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from faker import Faker
import requests

# API key to openweathermap with geolocation
API_KEY_WEATHER = "67c4244714a6b3622cd4844889e9728c"
# API key to opentripmap
API_KEY_TRIP = "5ae2e3f221c38a28845f05b6072cf50482464e992930cf4c2ace5cf2"
resp = requests.get("https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY_WEATHER}")


st.title('Weather App')

name = st.text_input('Enter your name', '')
if name:
    st.write(f'Hello {name}, nice weather we having?')
city = st.text_input('Enter the city you heading to: ', 'London')
if city:
    st.button('Check Weather')
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY_WEATHER}'
    rest_weather = requests.get(weather_url)
    data_weather = rest_weather.json()

    if rest_weather.status_code == 200 and 'main' in data_weather:
        temp = data_weather['main']['temp'] - 273.15
        humidity = data_weather['main']['humidity']
        cloud = data_weather['clouds']['all']
        st.write(f"* The weather in {city} is **{temp:.2f}°** with **{humidity}%** humidity. **{cloud}%** of the sky covered with clouds.  " )

        trip_url = f"https://api.opentripmap.com/0.1/en/places/geoname?name={city}&apikey={API_KEY_TRIP}"

        rest_trip = requests.get(trip_url)
        data_trip = rest_trip.json()
        population = data_trip.get("population", "Unknown")

        st.write(f"* Did you know that the population of {city} is **{population}**.")
    else:
        message = data_weather.get('message', 'City not found.')
        st.warning(f"Could not fetch weather data for '{city}'. Reason: {message}")

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