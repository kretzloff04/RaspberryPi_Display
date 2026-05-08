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



def read_expiration():
    file_reader = open("key_expiration.txt", 'r')
    string = file_reader.read()
    float_expire = float(string)

    file_reader.close()
    print("[read_expiration] Key expiration read and stored in variable")
    return float_expire

curr_key_expire = read_expiration()

def write_expiration(new_time):
    file_writer = open("key_expiration.txt", 'w')
    string_time = str(new_time)
    file_writer.write(string_time)

    print("[write_expiration] New time written to /key_expiration.txt")
    file_writer.close()


def get_key_json_data():

    if(time.time() > curr_key_expire):
        url = f"https://www.strava.com/oauth/token?client_id={STRAVA_CLIENT_ID}&client_secret={STRAVA_CLIENT_SECRET}&refresh_token={STRAVA_REFRESH_TOKEN}&grant_type=refresh_token"
        response = requests.post(url)
        data = response.json()

        write_expiration(data["expires_at"])

        print(f"[get_key_json_data] Updated expires time at to {data["expires_at"]}")
        print("[get_key_json_data] Access key expired, valid JSON request made")
        return data
    else:
        print("[get_key_json_data] Key still valid, no need to request for new access key")
        return None



def get_new_token(key_json):
    global STRAVA_CLIENT_ACCESS_TOKEN
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
