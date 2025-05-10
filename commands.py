import os
import datetime
import requests
import math
def add(*args):
    return sum(args)
def divide(a,b):
    return round(a/b,3)
    
def multiply(*args):
    total = 1
    for arg in args:
        total *= arg
    return total
def subtract(a,*args):

    return a - sum(args)
    
def rect_perimeter(l,w):
    return (2 * (l+w))
def rect_diagonal(l,w):
    return math.sqrt((math.pow(l,2) + math.pow(w,2)))
#print(f"(debug) text: {text}")
def get_date_time():
    x = datetime.datetime.now()
    return x
def get_weather_from_lat_long(lat,lon):
    weather = requests.post(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,rain,showers&timezone=auto")
    return weather.json
def get_local_weather():
    try:
        ip_response = requests.get("https://api.ipify.org/?format=plaintext")
        ip = ip_response.text.strip()
        #print(f"Public IP: {ip}")
        lat_long = requests.get(f"http://ip-api.com/json/{ip}")
        #print(f"Latitude and Longitude: {lat_long}")
        location = lat_long.json()
        lat = location["lat"]
        lon = location["lon"]
        weather = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,rain,showers&timezone=auto")
        #print(f"Weather: {weather}")

        return weather.json()
    except Exception as e:
        #print(e)
        return e