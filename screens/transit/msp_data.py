import json
import requests

GREEN_LINE_CODE = 902
WEST_BOUND_CODE = 1
EAST_BANK_STOP_CODE = "EABK"

#Returns JSON of all possible routes and their IDs
def get_all_route_data():
    url = "https://svc.metrotransit.org/nextripv2/routes"
    json = requests.get(url).json()
    print(json)

#Returns the possible directions that can be associated with the Green Line and each direction's ID
def get_green_directions():
    url = f"https://svc.metrotransit.org/nextripv2/directions/{GREEN_LINE_CODE}"
    json = requests.get(url).json()
    print(json)

#Gets all stops for the Green Line in the west bound direction
def get_stops():
    url = f"https://svc.metrotransit.org/nextripv2/stops/{GREEN_LINE_CODE}/{WEST_BOUND_CODE}"
    json = requests.get(url).json()
    print(json)

#Requests the API that displays all arrivals for the specific stop. In this case only using the East Bank Stop so only uses that specific code
#Returns an array of size 3 that holds JSON information. These arrivals are supposed to happen soonest of all scheduled arrivals
def get_three_arrivals():
    url = f"https://svc.metrotransit.org/nextripv2/{GREEN_LINE_CODE}/{WEST_BOUND_CODE}/{EAST_BANK_STOP_CODE}"
    data = requests.get(url).json()

    arr_of_arrivals = []
    i = 0
    num_trains = min(3, len(data["departures"]))
    while(i < num_trains)
        arr_of_arrivals.append(data["departures"][i])
        i += 1
    
    return arr_of_arrivals


def get_green_train_pos():
    url = f"https://svc.metrotransit.org/nextripv2/vehicles/{GREEN_LINE_CODE}"
    data = requests.get(url).json()

    coordinates_arr = []
    for i in range(len(data)):
        coordinates_arr.append((data[i]["latitude"], data[i]["longitude"]))
    
    return coordinates_arr



if __name__ == "__main__":
    print(get_green_train_pos())