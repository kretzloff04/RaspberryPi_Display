from dotenv import load_dotenv
import os
import requests
import json
import time

load_dotenv()


STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
STRAVA_CLIENT_ACCESS_TOKEN = os.getenv("STRAVA_CLIENT_ACCESS_TOKEN")
STRAVA_REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")

curr_key_expire = 1778277600

# key_url = "https://www.strava.com/oauth/token"

# information = {
#     "client_id": STRAVA_CLIENT_ID,
#     "client_secret": STRAVA_CLIENT_SECRET,
#     "code": 
# }

def get_key_json_data():
    if(time.time() > curr_key_expire):
        url = f"https://www.strava.com/oauth/token?client_id={STRAVA_CLIENT_ID}&client_secret={STRAVA_CLIENT_SECRET}&refresh_token={STRAVA_REFRESH_TOKEN}&grant_type=refresh_token"
        response = requests.post(url)
        data = response.json()
        print("[get_key_json_data] Access key expired, valid JSON request made")
        return data
    else:
        print("[get_key_json_data] Key still valid, no need to request for new access key")
        return None



def get_new_token(key_json):
    if(key_json == None):
        print("[get_new_token] Valid access token, no change")
        return None

    else:
        if(data["access_token"]):
            STRAVA_CLIENT_ACCESS_TOKEN = data["access_token"]
            print("[get_new_token] Access token changed")
        else:
            print("[get_new_token] Invalid request, access token not found")


data = get_key_json_data()
get_new_token(data)
