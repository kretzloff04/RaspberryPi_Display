import json
import requests

def test():
    url = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard?dates=20260513"

    data = requests.get(url).json()
    print(data)

def test2():
    url = "https://sports.core.api.espn.com/v2/sports/baseball/leagues/mlb/calendar"

    data = requests.get(url).json()
    print(data)

test()
