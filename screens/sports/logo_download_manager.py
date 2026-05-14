import os
import requests
import json
from PIL import Image
from io import BytesIO

#Used to get the correct API request URL depending on sport / league
#param sport: A string parameter that represents the sport / league that we want to generate logos for
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
    elif(sport == "mlb"):
        url = "https://sports.core.api.espn.com/v2/sports/baseball/leagues/mlb/teams"
    return url


#Uses the ESPN API to download logos for the specific {sport} input league.
#The sport parameter just specifies the league that we will be downloading the images from
#Overall order of functionality is as follows:
#1. Use the overall sport api url that gathers all teams from that league
#2. Because the teams are set up as: multiple pages containing ~25 api url references to the actual team information
#3. We must iterate while there are still pages to view
#4. Within this iteration, we want to check every single team on that specific page.
#5. We find the logo (if the team has one) and resize the image
#6. The image is saved into "assets/{sport}/" filepath.
def download_logos(sport):
    #Gets url based on sport using get_api_req helper method
    base_url = get_api_req(sport)

    #represents the json data for the sport / league's teams. Formatted in pages.
    #To access other pages must use the query "?page={pageNum}"
    req = requests.get(base_url).json()
    
    #Arr of dictionaries holding team references
    teams = req["items"]
    page_count = 1
    team_count = 1
    
    while(teams != []):
        url = base_url
        print(f"Page {page_count} / {req["pageCount"]}")
        for pair in teams:
            #All teams are mapped to '$ref'
            team_api_url = pair['$ref']


            #Because the dictionaries hold references to actual team JSON data, 
            #we must use that reference api_url to request from the api
            team_req_json = requests.get(team_api_url).json()
            team_name = team_req_json["slug"]
            file_name = team_name + "-logo.png"
            if(os.path.exists(f"../../assets/{sport}/{file_name}")):
                print(f"[{team_count}] {team_name} already has a file saved!")
                team_count += 1
                continue
                
            try:
                
                #Accesses the "default" team logo from logos dict
                logo_json = team_req_json["logos"]
                default_logo = logo_json[0]
                default_logo_href = default_logo['href']
                
                print(f"[{team_count}] Saving {file_name}...")

                #Uses the req library to request the reference to the default logo image 
                logo_request = requests.get(default_logo_href)

                #Resizes image using PIL library
                print(f"[{team_count}] Resizing...")
                img = Image.open(BytesIO(logo_request.content))
                img = img.resize((24,24))
                img.save(f"../../assets/{sport}/{file_name}")

                print(f"[{team_count}] Successfully saved!")


            #Handles teams that don't have a logo?
            except KeyError:
                print(f"[{team_count}] {team_name} doesn't have logo")
            
            finally:
                team_count += 1

        #Increments counter and handles url api for next page request
        page_count += 1
        url += f"?page={page_count}"
        print(url)
        req = requests.get(url).json()
        teams = req["items"]
        
        
download_logos("mlb")