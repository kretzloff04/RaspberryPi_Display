import json
import requests
import time

from datetime import datetime

def get_daily_data():
    date = get_curr_date()
    url = f"https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard?dates={date}"

    data = requests.get(url).json()
    print(data)


def get_curr_date():
    curr_dt = datetime.now()
    year = curr_dt.strftime("%Y")
    month = curr_dt.strftime("%m")
    day = curr_dt.strftime("%d")
    return f"{year}{month}{day}"




date_time_test()
