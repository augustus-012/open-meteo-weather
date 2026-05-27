import requests
from requests.exceptions import HTTPError
from pprint import pprint
import sys

latitude = 6.6137 # default
longitude = 3.3553 # default

def main():
    global latitude, longitude
    if len(sys.argv) == 3:
        latitude = float(sys.argv[1])
        longitude = float(sys.argv[2])

    try:
        url = "https://api.open-meteo.com/v1/forecast?"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "timezone": "auto",
            "current": ["temperature_2m", "rain", "showers", "is_day", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m", "pressure_msl", "surface_pressure", "snowfall"],
            "hourly": ["temperature_2m", "weather_code"]
        }
        response = requests.get(url=url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        """modify data"""
        # i. only 24 hours
        for var in data["hourly"]:
            data["hourly"][var] = data["hourly"][var][:24]
        # ii. clean up time
        data["current"]["time"] = data["current"]["time"].replace("T", " ")
        for i in range(len(data["hourly"]["time"])):
            data["hourly"]["time"][i] = data["hourly"]["time"][i].replace("T", " ")
        

        # current data and units, hourly data
        current = data["current"]
        current_units = data["current_units"]
        hourly = data["hourly"]

        # location
        place = data["timezone"].split("/")[1]

        # current variables
        time_of_day = "Day" if current["is_day"] else "Night"
        sea_level_pressure = f"{current['pressure_msl']} {current_units['pressure_msl']}"
        rain = f"{current['rain']} {current_units['rain']}"
        snow = f"{current['snowfall']} {current_units['snowfall']}"
        temperature = f"{current['temperature_2m']}{current_units['temperature_2m']}"
        time = current['time']
        wind_speed = f"{current['wind_speed_10m']} {current_units['wind_speed_10m']}"
        wind_direction = f"{current['wind_direction_10m']}{current_units['wind_direction_10m']}"
        surface_level_pressure = f"{current['surface_pressure']} {current_units['surface_pressure']}"

        # hourly values
        hourly_temperatures_today = [f"{temp}{current_units['temperature_2m']}" for temp in hourly["temperature_2m"]]
        hourly_times = hourly['time']
        hourly_weather_descriptions = [get_weather_description(code) for code in hourly["weather_code"]]

        # show current weather data
        title_len = 44
        value_len = 16
        line_len = title_len + value_len
        print("\n")
        print(f" THE WEATHER IN {place.upper()} ".center(line_len, "="))
        print("\n")
        print(" CURRENT WEATHER CONDITION ".center(line_len, "-"))
        print(f"{'Time of day:'.ljust(title_len)}{time_of_day.ljust(value_len)}")
        print(f"{'-'*line_len}")
        print(f"{'Time:'.ljust(title_len)}{time.ljust(value_len)}")
        print(f"{'-'*line_len}")
        print(f"{'Temperature:'.ljust(title_len)}{temperature.ljust(value_len)}")
        print(f"{'-'*line_len}")
        print(f"{'Rain:'.ljust(title_len)}{rain.ljust(value_len)}")
        print(f"{'-'*line_len}")
        print(f"{'Snow:'.ljust(title_len)}{snow.ljust(value_len)}")
        print(f"{'-'*line_len}")
        print(f"{'Wind speed:'.ljust(title_len)}{wind_speed.ljust(value_len)}")
        print(f"{'-'*line_len}")
        print(f"{'Wind direction:'.ljust(title_len)}{wind_direction.ljust(value_len)}")
        print(f"{'-'*line_len}")
        print(f"{'Surface level pressure:'.ljust(title_len)}{surface_level_pressure.ljust(value_len)}")
        print(f"{'-'*line_len}")
        print(f"{'Sea level pressure:'.ljust(title_len)}{sea_level_pressure.ljust(value_len)}")
        print(f"{'-'*line_len}")

        # show hourly temperatures
        value_len -= 10
        line_len = title_len + value_len
        print("\n")
        print(f" HOURLY TEMPERATURES TODAY IN {place.upper()} ".center(line_len, "-"))
        for _time, _temp in zip(hourly_times, hourly_temperatures_today):
            print(f"{_time.ljust(title_len)}{_temp.ljust(value_len)}")
            print(f"{"-"*line_len}")

        # show hourly weather description
        value_len += 16
        line_len = title_len + value_len
        print("\n")
        print(f" HOURLY WEATHER DESCRIPTIONS TODAY IN {place.upper()} ".center(line_len, "-"))
        for time_, desc in zip(hourly_times, hourly_weather_descriptions):
            print(f"{time_.ljust(title_len)}{desc.ljust(value_len)}")
            print(f"{"-"*line_len}")
        
        #pprint(data)
    except HTTPError as http_err:
        print(f"Error: {http_err}")
    except Exception as err:
        print(f"Other error occured: {err}")
    else:
        print("Success!")



def get_weather_description(weather_code):
    if weather_code == 0:
        return "Clear sky"
    elif weather_code in (1, 2, 3):
        if weather_code == 1:
            return "Mainly clear"
        elif weather_code == 2:
            return "Partly cloudy"
        elif weather_code == 3:
            return "Overcast"
    elif weather_code in (45, 48):
        return "Foggy"
    elif weather_code in (51, 53, 55):
        if weather_code == 51:
            return "Light drizzle"
        elif weather_code == 53:
            return "Moderate drizzle"
        elif weather_code == 55:
            return "Dense drizzle"
    elif weather_code in (61, 63, 65):
        if weather_code == 61:
            return "Slight rain"
        elif weather_code == 63:
            return "Moderate rain"
        elif weather_code == 65:
            return "Heavy rain"
    elif weather_code in (71, 73, 75):
        if weather_code == 71:
            return "Slight snow"
        elif weather_code == 73:
            return "Moderate snow"
        elif weather_code == 75:
            return "Heavy snow"
    elif weather_code in (80, 81, 82):
        if weather_code == 80:
            return "Slight rain shower"
        elif weather_code == 81:
            return "Moderate rain shower"
        elif weather_code == 82:
            return "Violent rain shower"
    elif weather_code == 95:
        return "Thunderstorm"
    elif weather_code in (96, 99):
        return "Thunderstorm with hail"

main()