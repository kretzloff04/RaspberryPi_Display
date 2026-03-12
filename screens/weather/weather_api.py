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
        self.time = ""
        self.date = ""

    def __init__(self, name, real_temp, feels_like_temp, description, time, date):
        self.name = name
        self.real_temp = real_temp
        self.feels_like_temp = feels_like_temp
        self.description = description
        self.time = time
        self.date = date


    def __str__(self):
        return_string = ""
        return_string += f"{self.name}: \n"
        return_string += f"Real Temperature: {self.real_temp}\n"
        return_string += f"Feels Like Temperature: {self.feels_like_temp}\n"
        return_string += f"Weather Description: {self.description}\n"

        if(self.time != "" and self.date != ""):
            return_string += f"Date: {self.date}\n"
            return_string += f"Time: {self.time}\n"

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
    print(req)

    #Pulls weather description (sunny, rainy, cloudy, etc)
    desc = req["weather"][0]["description"]

    #Extracts both air temp and feels like temp
    temp = req["main"]["temp"] 
    feels_temp = req["main"]["feels_like"]

    new_weather = CityWeather(city, temp, feels_temp, desc)

    return new_weather


#TODO Implement get future weather 

#Returns an array of CityWeather objects of  3 hour increments for the next 5 days

#1. Handles API req and url
#2. Iterates through "list" portion of api response (array of dictionaries representing each day's weather)
#3. Gathers data and formats
#4. Creates object and appends to arr
#5. Returns the array of CityWeather objects
def get_hourly_weather(city):
    coords = get_coords(city)

    api_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={coords[0]}&lon={coords[1]}&appid={WEATHER_API_KEY}&units=imperial"
    req = requests.get(api_url).json()

    weather_arr = []
    for i in range(len(req["list"])):
        #Assigns temp, feels_like, and description to the respective values listed in api
        temp = req["list"][i]["main"]["temp"]
        feels_temp = req["list"][i]["main"]["feels_like"]
        desc = req["list"][i]["weather"][0]["description"]
        

        #Retrieves "dt_txt" value from api (date/time in text format) and splits into [date, time]
        dt_base = req["list"][i]["dt_txt"]
        dt_split = dt_base.split(" ")

        #Edit the date to my format by grabbing date and splitting that by "-"
        date_base = dt_split[0]
        date_split = date_base.split("-")

        #Final format
        final_date = f"{date_split[1]}/{date_split[2]}"

        #Grabs time and splits based on ":"
        time_base = dt_split[1]
        time_split = time_base.split(":")
        tag = "AM"

        #Handles case when the time is in military format (hour + 12) -> ex: 15:42
        if(int(time_split[0]) > 12):
            time_split[0] = int(time_split[0]) - 12
            tag = "PM"
        
        #Handles midnight because api returns midnight as "00:00:00"
        elif(int(time_split[0]) == 0):
            time_split[0] = 12
        
        #Handles noon to make sure tag is represented as PM
        elif(int(time_split[0]) == 12):
            tag = "PM"
        
        #Final format of time
        final_time = f"{time_split[0]}:{time_split[1]} {tag}"

        new_weather = CityWeather(city, temp, feels_temp, desc, final_time, final_date)
        weather_arr.append(new_weather)
    
    return weather_arr
        



