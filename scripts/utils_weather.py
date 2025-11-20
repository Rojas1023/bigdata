# # scripts/utils_weather.py
# import os
# import requests
# from dotenv import load_dotenv

# load_dotenv()

# API_KEY = os.getenv("OPENWEATHER_API_KEY", "2d766fc0630c60dec177b391207e3e91")
# CITY = os.getenv("OPENWEATHER_CITY", "Bogota,CO")

# def get_current_weather(city=None):
#     city = city or CITY
#     url = "https://api.openweathermap.org/data/2.5/weather"
#     params = {"q": city, "appid": API_KEY, "units": "metric", "lang": "es"}
#     try:
#         r = requests.get(url, params=params, timeout=10)
#         r.raise_for_status()
#         j = r.json()
#         main = j.get("main", {})
#         wind = j.get("wind", {})
#         weather = j.get("weather", [{}])[0]
#         data = {
#             "temp": main.get("temp"),
#             "humidity": main.get("humidity"),
#             "pressure": main.get("pressure"),
#             "wind_speed": wind.get("speed"),
#             "weather_main": weather.get("main"),
#             "weather_desc": weather.get("description"),
#             "is_raining": ("rain" in (weather.get("main","").lower() or "") ) or ("rain" in (weather.get("description","").lower() or "")),
#             "raw": j
#         }
#         return data
#     except Exception as e:
#         print("Error weather:", e)
#         return None
