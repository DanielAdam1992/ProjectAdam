# ProjectAdam
# Project for DS20 Class. 
#  Weather & Time Checker App

This is a simple and interactive Streamlit application that allows users to:

- Get the current weather conditions (temperature, humidity, cloudiness) of any city.
- View the population of that city using the OpenTripMap API.
- Display a weather icon based on current conditions.
- Show a live map using Folium.
- Display your local time and the time in the selected city.

## Technologies Used

- Python
- Streamlit
- OpenWeatherMap API
- OpenTripMap API
- Folium (for maps)
- Pytz (for timezone conversion)

## How to Run

1. Clone the repository:
   ```clone to github desktop
   git clone https://github.com/DanielAdam1992/ProjectAdam
   cd ProjectAdam
Install dependencies with Poetry:


Copy
Edit
poetry install
Set your API keys in the code or via environment variables.

Run the app:

poetry run streamlit run main.py
API Keys Required
OpenWeatherMap

OpenTripMap
