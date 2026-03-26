import os
import requests
import json
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

# def get_next_train(stop, direction):
#     num_direction = 0
#     lower_dir = direction.lower()

#     if(lower_dir == "north" or lower_dir == "n"):
#         num_direction = 1
#     else:
#         num_direction = 5


#Retrieves all active train positions in json format
def get_all_active_trains():
    json_data = requests.get(TRAIN_POS_BASE_URL).json()
    print(json_data)

def get_all_train_pos(json_data):
    trains_arr = json_data["ctatt"]["route"]["train"]


