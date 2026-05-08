from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()


STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
STRAVA_CLIENT_ACCESS_TOKEN = os.getenv("STRAVA_CLIENT_ACCESS_TOKEN")
STRAVA_REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")

# key_url = "https://www.strava.com/oauth/token"

# information = {
#     "client_id": STRAVA_CLIENT_ID,
#     "client_secret": STRAVA_CLIENT_SECRET,
#     "code": 
# }

def get_new_token():
    url = f"https://www.strava.com/oauth/token?client_id={STRAVA_CLIENT_ID}&client_secret={STRAVA_CLIENT_SECRET}&refresh_token={STRAVA_REFRESH_TOKEN}&grant_type=refresh_token"
    response = requests.post(url)
    data = response.json()
    print(data)

    if(data["access_token"]):
        STRAVA_CLIENT_ACCESS_TOKEN = data["access_token"]
    else:
        print("Invalid request, access token not found")

get_new_token()
print(STRAVA_CLIENT_ACCESS_TOKEN)

