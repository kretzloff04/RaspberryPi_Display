import os
import requests
import json

def get_api_req(sport):
    url = ""
    if(sport == "cbb"):
        url = "https://sports.core.api.espn.com/v2/sports/basketball/leagues/mens-college-basketball/teams"
    elif(sport == "nfl"):
        url = "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/teams"
    elif(sport == "nhl"):
        url = "https://sports.core.api.espn.com/v2/sports/hockey/leagues/nhl/teams"
    elif(sport == "nba"):
        url = "https://sports.core.api.espn.com/v2/sports/basketball/leagues/nba/teams"
    elif(sport == "cfb"):
        url = "https://sports.core.api.espn.com/v2/sports/football/leagues/college-football/teams"
    return url



def download_logos(sport):
    url = get_api_req(sport)

    req = requests.get(url).json()
    teams = req["items"]
    for team in teams:
        print(team)

download_logos("cbb")