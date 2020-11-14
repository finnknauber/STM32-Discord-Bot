#get_launches.py
import requests
import datetime
import json
import os

def format_time(time_string):
    year=int(time_string[:4])
    month=int(time_string[5:7])
    day=int(time_string[8:10])
    hour=int(time_string[11:13])
    minute=int(time_string[14:16])

    time = datetime.datetime(year, month, day, hour, minute)
    return time

def get_launch_json():
    requestData = requests.get('https://ll.thespacedevs.com/2.0.0/launch/upcoming?mode=list')
    if requestData.status_code == 200:
        return requestData.json()
    return get_file_json()


def write_launches(launch_data):
    if launch_data:
        try:
            dumplaunch_data = json.dumps(launch_data, skipkeys=True, indent=4)
            with open("launches.json", "w") as json_file:
                json_file.seek(0)
                json_file.write(dumplaunch_data)
                json_file.truncate()
        except:
            print("Failed when trying to write to json file")
    return launch_data


def get_upcoming(launch_data):
    launches = "**Upcoming launches:**\n\n"
    if "results" in launch_data:
        for launch in launch_data["results"]:
            if launch["status"]["name"] != "Success":
                launch_string="• **" + launch["name"] + "**"
                if "lsp_name" in launch:
                    launch_string+=" by ***" + launch["lsp_name"] + "***"

                utc_time = datetime.datetime.utcnow()
                utc_time = datetime.datetime(utc_time.year, utc_time.month, utc_time.day, utc_time.hour, utc_time.minute)
                time = format_time(launch["net"]) - utc_time
                
                launch_string+=" is launching in T-" + str(time)[:-3]
                launch_string+=". \nThe current mission status is **" + launch["status"]["name"] + "**"
                launches+=launch_string + "\n"

    else:
        return ""

    return launches


def get_file_json():
    with open("launches.json") as requestData:
        try:
            requestData = json.loads(requestData.read())
            return requestData
        except:
            print("Failed while trying to read file")
    return {}


def update_launches():
    requestData = get_file_json()
    if requestData != {}:
        launch_data = get_launch_json()
        if requestData != launch_data and launch_data != {}:
            write_launches(launch_data)

update_launches()

