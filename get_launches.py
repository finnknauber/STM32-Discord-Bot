#get_launches.py
import requests
import json
import os

def get_launch_json():
    requestData = requests.get('https://ll.thespacedevs.com/2.0.0/launch/upcoming?mode=list')
    if requestData.status_code == 200:
        return requestData.json()
    return {}

def write_launches(launch_data):
    if launch_data:
        try:
            launch_data = json.dumps(launch_data, skipkeys=True, indent=4)
            with open("/launches.json", "w") as json_file:
                json_file.seek(0)
                json_file.write(launch_data)
                json_file.truncate()
        except:
            print("Failed when trying to write to json file")

def get_upcoming(launch_data):
    launches = "**Upcoming launches:**\n\n"
    if "results" in launch_data:
        for launch in launch_data["results"]:
            if launch["status"]["name"] != "Success":
                launch_string="• **" + launch["name"] + "**"
                if "lsp_name" in launch:
                    launch_string+=" by *" + launch["lsp_name"] + "*"

                launch_string+=" is launching on " + launch["net"]
                launch_string+=". \nThe current mission status is **" + launch["status"]["name"] + "**"
                launches+=launch_string + "\n\n"

    return launches

def get_launches(launch_data):
    launches = ""
    if "results" in launch_data:
        for launch in launch_data["results"]:
            if launch["status"]["name"] != "Success":
                launch_string = ""

                launch_string+=launch["name"]

                if "lsp_name" in launch:
                    launch_string+=" by " + launch["lsp_name"]
                
                launch_string+=" is launching on " + launch["net"]

                if "launcher" in launch:
                    if launch["launcher"]:
                        launch_string+=" using " + launch["launcher"]

                if "pad" in launch:
                    launch_string+=" from " + launch["pad"]
                    launch_string+=" in " + launch["location"]
                
                if "landing" in launch:
                    if launch["landing"]:
                        launch_string+=" a landing will be attempted on/at " + launch["landing"]

                launch_string+=". \nThe current mission status is " + launch["status"]["name"]

                if "mission_type" in launch:
                    launch_string+="\nThe missions purpose is " + launch["mission_type"]

                if "orbit" in launch:
                    if launch["orbit"]:
                        launch_string+=".\nIt is headed to " + launch["orbit"]

                if "infographic" in launch:
                    if launch["infographic"]:
                        launch_string+="\n"+launch["infographic"]
                    elif "image" in launch:
                        if launch["image"]:
                            launch_string+="\n"+launch["image"]

                elif "image" in launch:
                    if launch["image"]:
                        launch_string+="\n"+launch["image"]

                launches+=launch_string + "\n\n"

    return launches

def get_file_json():
    with open("/launches.json") as requestData:
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

