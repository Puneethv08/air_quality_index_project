import streamlit as st
import requests
from datetime import datetime, timezone, timedelta
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO

API_KEY = "d11c751b2149eae221f04d77c5f1db60"

def fetch_geo(city_name, api_key=API_KEY):
    """Get latitude and longitude of a city using OpenWeatherMap Geocoding API."""
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    if data:
        return data[0]['lat'], data[0]['lon']
    else:
        return None, None

def fetch_air_quality(lat, lon, api_key=API_KEY):
    """Get air pollution data using OpenWeatherMap Air Pollution API."""
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)
    return response.json()

def plot_pollutants(pollutants, city_name, timestamp_unix):
    """Plot bar chart for pollutant concentrations with improved style and info."""
    names = [gas.upper() for gas in pollutants.keys()]
    values = list(pollutants.values())

    pollutant_info = {
        "CO": "Carbon Monoxide — from fuel combustion",
        "NO": "Nitric Oxide — from vehicles & industry",
        "NO2": "Nitrogen Dioxide — causes respiratory issues",
        "O3": "Ozone — harmful at ground level",
        "SO2": "Sulfur Dioxide — from burning fossil fuels",
        "PM2_5": "Fine Particles (<2.5µm) — health hazard",
        "PM10": "Coarse Particles (<10µm) — dust, pollen",
        "NH3": "Ammonia — from agriculture & waste"
    }

    dt_utc = datetime.fromtimestamp(timestamp_unix, tz=timezone.utc)
    ist_offset = timedelta(hours=5, minutes=30)
    ist = timezone(ist_offset)
    dt_local = dt_utc.astimezone(ist)
    timestamp_str = dt_local.strftime("%Y-%m-%d %I:%M:%S %p")

    plt.style.use('seaborn-v0_8-deep')
    fig, ax = plt.subplots(figsize=(12, 7))

    bars = ax.bar(names, values, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', 
                                        '#9467bd', '#8c564b', '#e377c2', '#7f7f7f'], edgecolor='black')

    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, value + 0.5, f"{value:.2f}", 
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.set_title("Air Pollutants Levels (μg/m³)", fontsize=18, fontweight='bold', color='#333333', pad=15)
    ax.set_xlabel("Pollutants", fontsize=14, fontweight='bold')
    ax.set_ylabel("Concentration (μg/m³)", fontsize=14, fontweight='bold')

    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(fontsize=12, fontweight='bold')
    plt.yticks(fontsize=12)

    description_text = "\n".join([f"{k}: {v}" for k, v in pollutant_info.items()])
    plt.gcf().text(1.02, 0.5, description_text, fontsize=10, va='center', ha='left', linespacing=1.5)

    ax.text(0.5, -0.15, f"Data captured on: {timestamp_str} ({city_name.title()})", 
            transform=ax.transAxes, fontsize=11, fontweight='bold', color='#222222', ha='center')

    plt.tight_layout()
    return fig

# Streamlit app starts here
st.title("🌍 Live Air Quality Index (AQI) Dashboard")

city = st.text_input("Enter a city name:", "Bengaluru")

if city:
    lat, lon = fetch_geo(city)
    if lat is not None and lon is not None:
        data = fetch_air_quality(lat, lon)
        if 'list' in data and len(data['list']) > 0:
            aqi = data['list'][0]['main']['aqi']
            aqi_category = {
                1: "Good",
                2: "Fair",
                3: "Moderate",
                4: "Poor",
                5: "Very Poor"
            }
            st.subheader(f"AQI for {city.title()}: {aqi} ({aqi_category.get(aqi, 'Unknown')})")

            pollutants = data['list'][0]['components']
            timestamp_unix = data['list'][0]['dt']
            fig = plot_pollutants(pollutants, city, timestamp_unix)
            st.pyplot(fig)

            location_df = pd.DataFrame({'lat': [lat], 'lon': [lon]})
            st.map(location_df)

            # Prepare data for CSV download
            df = pd.DataFrame([pollutants])
            df.insert(0, "City", city.title())
            dt_utc = datetime.fromtimestamp(timestamp_unix, tz=timezone.utc)
            ist_offset = timedelta(hours=5, minutes=30)
            ist = timezone(ist_offset)
            dt_local = dt_utc.astimezone(ist)
            df.insert(1, "Timestamp", dt_local.strftime("%Y-%m-%d %I:%M:%S %p"))

            csv_data = df.to_csv(index=False).encode('utf-8')
            filename = f"air_quality_{city.title()}_{dt_local.strftime('%Y-%m-%d_%I-%M-%S_%p')}.csv"

            st.download_button(
                label="Download AQI Data as CSV",
                data=csv_data,
                file_name=filename,
                mime='text/csv'
            )

        else:
            st.error("No air quality data found for this location.")
    else:
        st.error("City not found. Please enter a valid city name.")
