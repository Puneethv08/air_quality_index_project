Air Quality Index Dashboard 🌍

A Streamlit-based interactive dashboard to monitor real-time Air Quality Index (AQI) for different cities, visualize pollutant levels, and download data in CSV format.



📌 Features

Live AQI Data: Fetches real-time AQI and pollutant data from an API.

AQI Classification: Shows AQI value with category (Good, Moderate, Poor, etc.).

Pollutant Visualization: Displays pollutant levels in a bar chart.

Map View: Displays the city’s location on a map.

Data Download: Download AQI data as a CSV file with city name \& timestamp in the filename.



🛠 Tech Stack

Python 3

Streamlit – for interactive UI

Requests – for fetching API data

Pandas – for data processing

Plotly – for visualizations

🚀 Installation \& Setup

Clone the repository:

git clone https://github.com/Puneethv08/air\_quality\_index\_project.git

cd air\_quality\_index\_project

Install dependencies:

pip install -r requirements.txt

Run the app:

streamlit run aqi\_dashboard.py

📊 Example Output

AQI Value: 85 – Moderate

Pollutant chart with PM2.5, PM10, NO₂, SO₂ levels

City location shown on map

Downloaded CSV: air\_quality\_Bengaluru\_2025-08-10.csv

📌 API Used

OpenWeatherMap Air Pollution API – for live AQI data

📄 License
This project is open-source and available under the MIT License.





