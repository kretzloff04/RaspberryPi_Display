import json

class Summary:
    def __init__(self, hours, total_in, total_out, stakes):
        self.hours = hours
        self.total_in = total_in
        self.total_out = total_out
        self.stakes = stakes
        
        self.profit = (total_out - total_in)

        self.dollar_hour = self.profit / self.hours
        self.bb_hour = self.calculate_bb_hour()


    def calculate_bb_hour(self):
        if(len(self.stakes) > 1):
            return 0

        split = self.stakes[0].split("/")
        bb_str = split[1]
        bb = int(bb_str)

        return (self.dollar_hour / bb)

def gather_session_data():
    file = open("raw_poker_data.json")
    json_data = json.loads(file.read())
    print(json_data["sessions"][0])
    
# def gather_summary_data():


# def update_session_data():

#Finds all stakes played in raw_poker_data and returns an array of said stakes
def gather_all_stakes_played():
    #Opens and reads data
    file = open("raw_poker_data.json")
    json_data = json.loads(file.read())
    return_arr = []

    #Iterates through adding to set if not already inside
    stakes = set()
    for session in json_data["sessions"]:
        if(session["game"]["stakes"] not in stakes):
            stakes.add(session["game"]["stakes"])
    
    #Returns as arr
    for stake in stakes:
        return_arr.append(stake)

    file.close()
    return return_arr
    
        
#Method that creates uses the Summary OBJECT from "create_summary_by_stakes"
#and writes that to poker_summary.json. This holds a summarized
#version of the raw data collected from raw_poker_data.json
def write_overall_summary_json():
    summary = create_summary_by_stakes("ALL")
    file_path = "poker_summary.json"

    file_reader = open(file_path, 'r')
    json_data = json.loads(file_reader.read())
    
    overall_summary_data = json_data["overall_summary"]

    print("Altering Data...")
    overall_summary_data["stakes"] = summary.stakes
    overall_summary_data["hours"] = summary.hours
    overall_summary_data["profit"] = summary.profit
    overall_summary_data["total_buy_in"] = summary.total_in
    overall_summary_data["total_cash_out"] = summary.total_out
    overall_summary_data["bb/hr"] = summary.bb_hour
    overall_summary_data["$/hr"] = summary.dollar_hour
    
    print(f"Writing Back to {file_path}")
    file_writer = open(file_path, 'w')
    json.dump(json_data, file_writer, indent=4)


    file_reader.close()
    file_writer.close()



def write_stakes_summary(stakes):
    summary = create_summary_by_stakes(stakes)



#Creates a summary OBJECT from the raw data in raw_poker_data
#Takes in "stakes" which is a string that determines what stakes
#the summary will be created for

def create_summary_by_stakes(stakes):
    file = open("raw_poker_data.json")
    json_data = json.loads(file.read())

    hours = 0
    total_in = 0
    total_out = 0
    stakes_seen = set()

    for session in (json_data["sessions"]):
        #Only adds the stats if we want all stakes or if curr stakes match the input stakes param
        if(stakes == "ALL" or session["game"]["stakes"] == stakes):
            #Adds data
            hours += session["game"]["hours_played"]
            total_in += session["game"]["in"]
            total_out += session["game"]["out"]
            stakes_seen.add(session["game"]["stakes"])

        
    file.close()
    #Alters to array data structure
    stakes_arr = []
    for stake in stakes_seen:
        stakes_arr.append(stake)
    
    print("Creating Summary Object...")
    return Summary(hours, total_in, total_out, stakes_arr)


#TODO: Think about writing a method that handles all file reading and passes the json data to the rest of the methods.
#This can reduce number of reads and overall read time

write_overall_summary_json()