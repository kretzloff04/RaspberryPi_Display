from dotenv import load_dotenv
import os
import requests
import json
import time

load_dotenv()


STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
STRAVA_REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")

ATHLETE_ID = 186483013

def read_access_key():
    file_reader = open("keys_file.txt", 'r')
    access_token = file_reader.read()
    print("[read_access_key] Reading access key from /keys_file.txt")


    file_reader.close()
    
    return access_token

STRAVA_CLIENT_ACCESS_TOKEN = read_access_key()

def write_access_key(new_access_key):
    file_writer = open("keys_file.txt", 'w')

    file_writer.write(new_access_key)
    print("[write_access_key] Writing new access key to /keys_file.txt")

    file_writer.close()


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
            write_access_key(data["access_token"])
            print("[get_new_token] Access token changed")
        else:
            print("[get_new_token] Invalid request, access token not found")



def athlete_api_req():
    headers = {'Authorization': f"Bearer {STRAVA_CLIENT_ACCESS_TOKEN}"}
    url = f"https://www.strava.com/api/v3/athletes/{ATHLETE_ID}/stats"

    response = requests.get(url, headers=headers)
    data = response.json()

    return data

def overall_running_stats(athlete_data):
    return athlete_data["all_run_totals"]


def overall_biking_stats(athlete_data):
    return athlete_data["all_ride_totals"]


def recent_activities():
    headers = {'Authorization': f"Bearer {STRAVA_CLIENT_ACCESS_TOKEN}"}
    url = f"https://www.strava.com/api/v3/athlete/activities"

    response = requests.get(url, headers=headers)
    data = response.json()

    print(data)


data = get_key_json_data()
get_new_token(data)

# get_overall_stats()
recent_activities()