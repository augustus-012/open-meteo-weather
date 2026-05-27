# Open-Meteo Weather CLI

A command-line weather tool built with Python that fetches real-time weather data using the [Open-Meteo API](https://open-meteo.com/).

## Features
- Current weather conditions (temperature, rain, snow, wind, pressure)
- Hourly temperatures for today
- Hourly weather descriptions for today

## Usage

Default (Lagos):
py open_meteo.py

Custom location:
py open_meteo.py <latitude> <longitude>

Example (Tripoli):
py open_meteo.py 31.0194 15.7381

## Requirements
- Python 3
- requests library (`pip install requests`)
