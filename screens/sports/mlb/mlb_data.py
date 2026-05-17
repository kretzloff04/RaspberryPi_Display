import json
import requests
import time

from datetime import datetime

CUBS_ID = 16

class Game:
    self.cubsRuns = 0
    self.opposingRuns = 0
    self.inning = 1
    def __init__(self, opposingTeam, cubs_home):
        self.opposingTeam = opposingTeam
        self.cubs_home = cubs_home
        


def get_curr_date():
    curr_dt = datetime.now()
    year = curr_dt.strftime("%Y")
    month = curr_dt.strftime("%m")
    day = curr_dt.strftime("%d")
    return f"{year}{month}{day}"

def request_api():
    date = get_curr_date()
    url = f"https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard?dates={date}"

    data = requests.get(url).json()
    return data

# def get_cubs_schedule():
#     url = f"https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/teams"

#     data = requests.get(url).json()
#     print(data)

def create_game(data):
    for i in range(len(data["events"])):
        name = data["events"][i]["name"]
        split_short_name = short_name.split(" at ")
        
        opposing_team = ""
        cubs_home = False
        if(split_short_name[0] == "Chicago Cubs" or split_short_name[1] == "Chicago Cubs"):

            if(split_short_name[0] == "Chicago Cubs"):
                opposing_team = split_sort_name[1]

                
            elif(split_short_name[1] == "Chicago Cubs"):
                opposingTeam = split_sort_name[0]
                cubs_home = True

            return Game(opposing_team, cubs_home)
    
    print("No cubs game today, Game object not created")
    return None

def update_runs(data):
    game_data = data["events"][]

