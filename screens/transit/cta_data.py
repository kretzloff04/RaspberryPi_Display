import os
import requests
import json
import time

from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

CTA_BUS_API_KEY = os.getenv("CTA_BUS_API_KEY")
CTA_TRAIN_API_KEY = os.getenv("CTA_TRAIN_API_KEY")

#base api url for the positions of all trains on red line route.
TRAIN_POS_BASE_URL = f"http://lapi.transitchicago.com/api/1.0/ttpositions.aspx?key={CTA_TRAIN_API_KEY}&rt=red&outputType=JSON"

#base api url for arrivals at specified station (mapid must be appended)
TRAIN_ARRIVALS_URL = f"http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key={CTA_TRAIN_API_KEY}&outputType=JSON"

#CAN ALSO ADD API URL FOR FOLLOWING A SPECIFIC TRAIN

#Station_To_Code for the redline. These codes are for the STOPS. this means it represents the data for both the
#north and southbound trains.
STC_RED = {
    "Howard": 40900,
    "Jarvis": 41190,
    "Morse": 40100,
    "Loyola": 41300,
    "Granville": 40760,
    "Thorndale": 40880,
    "Bryn Mawr": 41380,
    "Berwyn": 40340,
    "Argyle": 41200,
    "Lawrence": 40770,
    "Wilson": 40540,
    "Sheridan":40080,
    "Addison": 41420,
    "Belmont": 41320,
    "Fullerton": 41220,
    "North/Clybourn": 40650,
    "Clark/Division":40630 ,
    "Chicago": 41450,
    "Grand":40330 ,
    "Lake": 41660,
    "Monroe": 41090,
    "Jackson": 40560,
    "Harrison": 41490,
    "Roosevelt":41400 ,
    "Cermark-Chinatown": 41000,
    "Sox-35th": 40190,
    "47th": 41230,
    "Garfield": 41170,
    "63rd": 40910,
    "69th": 40990,
    "79th": 40240,
    "87th": 41430,
    "95th/Dan Ryan": 40450
}


class Arrival:
    def __init__(self, eta, final_dest, tracked_station):
        self.eta = eta
        self.final_dest = final_dest
        self.tracked_station = tracked_station

    def __str__(self):
        string = ""
        string += f"ETA: {self.eta}\n"
        string += f"Final Destination: {self.final_dest}\n"
        string += f"Tracked Station: {self.tracked_station}\n"
        return string

#Grabs the json data for the given stop so we dont't have to continuously make requests
def get_arrivals_json(stop):
    map_id = STC_RED[stop]
    TRAIN_ARRIVALS_URL_NEW = TRAIN_ARRIVALS_URL + f"&mapid={map_id}"
    
    json_data = requests.get(TRAIN_ARRIVALS_URL_NEW).json()
    return json_data


#Takes arrival time in format of "HH:MM:SS" and compares it to current time to find the difference.
#This difference represents the ETA.
def formulate_arrival_time(arrival_str):
    curr_time = datetime.now()
    print(f"Curr Time: {curr_time}")
    
    arrival_time = datetime.strptime(arrival_str, "%H:%M:%S")
    

    arrival_time = arrival_time.replace(
        year = curr_time.year,
        month = curr_time.month,
        day = curr_time.day
    )
    difference = arrival_time - curr_time
    difference_str = str(difference)
    split = difference_str.split(":")

    mins = split[1]
    seconds = split[2][0:2]
    print(f"{mins}:{seconds}")
    return f"{mins}:{seconds}"
 
    

#Creates 3 "Arrival" objects and adds them to an array that is returned. These 3 Arrival objects represent the next 3
#trains to arrive at the input stop (from the json data input). 
def get_next_trains(json_data):
    eta_arr = json_data["ctatt"]["eta"]

    arrivals_arr = []
    count = 0
    time_diff = ""
    final_dest = ""
    tracked_station = ""
    time_generated = ""
    #Grabs 3 Arrival objects
    while(count < 3):
        #Grabs the arrival date/time and splices the array to only take the actual time
        overall_time = eta_arr[count]["arrT"]
        predicted_arrival = overall_time[11:]
        
        #Formats the time and grabs final destination and tracked station
        time_diff = formulate_arrival_time(predicted_arrival)
        final_dest = eta_arr[count]["destNm"]
        tracked_station = eta_arr[count]["staNm"]

        #Creates object and adds to array
        curr_arrival = Arrival(time_diff, final_dest, tracked_station)
        arrivals_arr.append(curr_arrival)

        count += 1
    
    return arrivals_arr






#Retrieves all active train positions in json format
def get_train_pos_json():
    json_data = requests.get(TRAIN_POS_BASE_URL).json()
    return json_data

#returns arr of positions of current trains in format of tuple ()
def get_all_train_pos(json_data):
    trains_arr = json_data["ctatt"]["route"][0]["train"]

    coordinates = []

    for train in trains_arr:
        float_lat = float(train["lat"])
        float_lon = float(train["lon"])
        coordinates.append((float_lat, float_lon))
    
    return coordinates



if __name__ == "__main__":
    # json = get_train_pos_json()
    
    # coords = get_all_train_pos(json)
    # print(coords)

    json_data = get_arrivals_json("Granville")
    arrivals_arr = get_next_trains(json_data)
    for i in range(len(arrivals_arr)):
        print(arrivals_arr[i])
        

