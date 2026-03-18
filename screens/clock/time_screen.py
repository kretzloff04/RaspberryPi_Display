import time
from datetime import datetime

#Fetches current CST time in the {hour}:{minute} format
def get_current_time():
    curr_dt = datetime.now()
    hour_str = curr_dt.strftime("%H") 
    minute_str = curr_dt.strftime("%M")
    day_night = "AM"

    hour_int = int(hour_str)

    #Converts 24 hour / military time 
    if(hour_int > 12):
        hour_int -= 12
        day_night = "PM"
    
    overall_time = f"{hour_int}:{minute_str} {day_night}"

    return overall_time

def get_current_date():
    curr_dt = datetime.now()

    month_str = curr_dt.strftime("%b")
    day_str = curr_dt.strftime("%d")

    overall_time = f"{month_str} {day_str}"

    return overall_time


def display_time():
    pass


# print(get_current_time())
# print(get_current_date())
