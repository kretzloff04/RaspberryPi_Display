import json

class Summary:
    def __init__(self, hours, total_in, total_out, stakes, sessions):
        self.hours = hours
        self.total_in = total_in
        self.total_out = total_out
        self.stakes = stakes
        self.sessions = sessions
        
        self.profit = (total_out - total_in)
        
        if(hours > 0):
            self.dollar_hour = self.profit / self.hours
            self.dollar_hour = round(self.dollar_hour, 2)
        else:
            self.dollar_hour = 0
        
        self.bb_hour = self.calculate_bb_hour()
        self.bb_hour = round(self.bb_hour, 2)

        self.roi = round((self.profit / self.total_in) * 100, 2)


    def calculate_bb_hour(self):
        if(len(self.stakes) != 1):
            return 0

        split = self.stakes[0].split("/")
        bb_str = split[1]
        bb = float(bb_str)

        return (self.dollar_hour / bb)
    
    def __str__(self):
        string = "_______________________\n"
        string += f"Hours: {self.hours}\n"
        string += f"Total Buy Ins: {self.total_in}\n"
        string += f"Total Cash Out: {self.total_out}\n"
        string += f"Profit: {self.profit}\n"
        string += f"Stakes: {self.stakes}\n"
        string += f"bb/hr: {self.bb_hour}\n"
        string += f"$/hr: {self.dollar_hour}\n"
        string += f"ROI: {self.roi}\n"
        string += "_______________________"

        return string





def load_data():
    file = open("raw_poker_data.json")

    print("Loading raw json data from: raw_poker_data.json")
    raw_json_data = json.loads(file.read())

    file.close()
    return raw_json_data

#Finds all stakes played in raw_poker_data and returns an array of said stakes
def gather_all_stakes_played(json_data):
    #Opens and reads data

    return_arr = []

    #Iterates through adding to set if not already inside
    stakes = set()
    for session in json_data["sessions"]:
        if(session["game"]["stakes"] not in stakes):
            stakes.add(session["game"]["stakes"])
    
    #Returns as arr
    for stake in stakes:
        return_arr.append(stake)

    return return_arr
    
        
#Method that creates uses the Summary OBJECT from "create_summary_by_stakes"
#and writes that to poker_summary.json. This holds a summarized
#version of the raw data collected from raw_poker_data.json
def write_overall_summary_json(raw_json_data):
    summary = create_summary_by_stakes("ALL", raw_json_data)
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
    overall_summary_data["ROI"] = summary.roi
    overall_summary_data["sessions"] = summary.sessions
    
    print(f"Writing Back to {file_path}")
    file_writer = open(file_path, 'w')
    json.dump(json_data, file_writer, indent=4)


    file_reader.close()
    file_writer.close()





#Populates the "summaries_by_stakes" attribute in "poker_summary.json"
#Does this by opening a read file, reading in the json data, iterating 
#over every single summary and adjusting the JSON data. This json data is 
#then "dumped" back to the file at the end of checking every single stake summary
def write_all_stakes_summary(raw_json_data):
    #opens the reader file to read unchanged data (overall_summary for ex)
    file_path = "poker_summary.json"
    file_reader = open(file_path)
    summary_json = json.loads(file_reader.read())

    #accesses "summaries_by_stakes" object (arr of summaries)
    summaries_by_stakes_arr = summary_json["summaries_by_stakes"]

    

    #iterates through each summary and adjusts the json data 
    #by creating the summary for that stake
    for stake_summary in summaries_by_stakes_arr:
        curr_stakes = stake_summary["stakes"][0]

        #creates summary for said stakes. 
        summary_obj = create_summary_by_stakes(curr_stakes, raw_json_data)
        print(summary_obj)

        #Adjusts json data
        stake_summary["hours"] = summary_obj.hours
        stake_summary["profit"] = summary_obj.profit
        stake_summary["total_buy_in"] = summary_obj.total_in
        stake_summary["total_cash_out"] = summary_obj.total_out
        stake_summary["bb/hr"] = summary_obj.bb_hour
        stake_summary["$/hr"] = summary_obj.dollar_hour
        stake_summary["ROI"] = summary_obj.roi
        stake_summary["sessions"] = summary_obj.sessions

        #writes entire json object back to file
    
    file_writer = open(file_path, 'w')
    json.dump(summary_json, file_writer, indent=4)


    file_reader.close()
    file_writer.close()



#Creates a summary OBJECT from the raw data in raw_poker_data
#Takes in "stakes" which is a string that determines what stakes
#the summary will be created for
def create_summary_by_stakes(stakes, raw_json_data):
    # file = open("raw_poker_data.json")
    # json_data = json.loads(file.read())

    hours = 0
    total_in = 0
    total_out = 0
    num_sessions = 0
    stakes_seen = set()

    print("Parsing json data")
    for session in (raw_json_data["sessions"]):

        #Only adds the stats if we want all stakes or if curr stakes match the input stakes param
        if(stakes == "ALL" or session["game"]["stakes"] == stakes):
            #Adds data
            hours += session["game"]["hours_played"]
            total_in += session["game"]["in"]
            total_out += session["game"]["out"]
            num_sessions += 1
            stakes_seen.add(session["game"]["stakes"])

  
    #Alters to array data structure
    stakes_arr = []
    for stake in stakes_seen:
        stakes_arr.append(stake)
    
    print("Creating Summary object...")
    print(f"stakes: {stakes}")
    print(f"hours: {hours}")
    print(f"total_in: {total_in}")
    print(f"total_out: {total_out}")

    return Summary(hours, total_in, total_out, stakes_arr, num_sessions)

#TODO: Add profit/sessions method that formulates data to allow for easy graphing.

if __name__ == "__main__":
    raw_json_data = load_data()
    write_all_stakes_summary(raw_json_data)
    write_overall_summary_json(raw_json_data)