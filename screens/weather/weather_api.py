from dotenv import load_dotenv
import os
import requests

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

class CityWeather:
    
    def __init__(self, name, real_temp, feels_like_temp, description):
        self.name = name
        self.real_temp = real_temp
        self.feels_like_temp = feels_like_temp
        self.description = description

    def __str__(self):
        return_string = ""
        return_string += f"{self.name}: \n"
        return_string += f"Real Temperature: {self.real_temp}\n"
        return_string += f"Feels Like Temperature: {self.feels_like_temp}\n"
        return_string += f"Weather Description: {self.description}"

        return return_string

    
    


#param: city -> A string input that represents the city that we want to request
#This city is mapped to a tuple of coords that is used in the input for the api request
def get_coords(city):
    coords = ()
    if(city == "CHI"):
        coords = (41.996461, -87.671934)
    
    elif(city == "MSP"):
        coords = (44.982061, -93.234426)
    
    elif(city == "NYC"):
        coords = (40.747097, -73.986391)
    
    #NOLA
    else:
        coords = (29.963883, -90.068428)
    
    return coords

#param: city -> A string input that represents the city that we want to request
#The "get_curr_weather" method is used to request the api to get info on the city's real temp, feels like temp, and general
#descriptions of the current weather. This data is returned as a "CityWeather" object.
def get_curr_weather(city):
    #retrieves coordinates for specified city
    coordinates = get_coords(city)
 
    #Adds coordinates and weather api key to api url
    api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={coordinates[0]}&lon={coordinates[1]}&appid={WEATHER_API_KEY}&units=imperial"
    req = requests.get(api_url).json()

    #Pulls weather description (sunny, rainy, cloudy, etc)
    desc = req["weather"][0]["description"]

    #Extracts both air temp and feels like temp
    temp = req["main"]["temp"] 
    feels_temp = req["main"]["feels_like"]

    new_weather = CityWeather(city, temp, feels_temp, desc)

    return new_weather


#TODO Implement get future weather 
    

