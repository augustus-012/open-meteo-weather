# Open-Meteo Weather CLI
A Python command-line tool that fetches real-time weather data for any location on Earth.

## Features
- Accurate city name detection using reverse geocoding
- Current weather conditions (temperature, rain, snow, wind speed, wind direction, pressure)
- Hourly temperatures for today (24 hours)
- Hourly weather descriptions for today (clear, cloudy, drizzle, rain, snow, thunderstorm, etc.)
- Defaults to your current location automatically
- Works for any location on Earth — cities, oceans, mountains, and more

## Usage

Default (your current location):
```
py open_meteo.py
```
Custom location:
```
py open_meteo.py <latitude> <longitude>
```
Examples:
```
py open_meteo.py 78.2232 15.6267
py open_meteo.py -33.8688 151.2093
```

## Requirements
- Python 3
- requests library (`pip install requests`)

## APIs Used
- [Open-Meteo](https://open-meteo.com/) — weather data
- [BigDataCloud](https://www.bigdatacloud.com/) — reverse geocoding
