#get_launches.py
import requests
import json

def serializeTime(timeString):
    months = ["January","February","March","April","May","Juni","July","August","September","October","November","Dezember"]
    if timeString:
        try:
            time = {}
            time["day"] = int(timeString.split(",")[0].split(" ")[-1])
            time["month"] = months.index( timeString.split(" ")[0] ) + 1
            time["year"] = int( timeString.split(",")[-1].strip().split(" ")[0] )
            time["timezone"] = timeString.split(" ")[-1]
            time["hour"] = int( timeString.split(" ")[-2].split(":")[0] )
            time["minute"] = int( timeString.split(" ")[-2].split(":")[1] )
            time["second"] = int( timeString.split(" ")[-2].split(":")[2] )

        except:
            time = None
            print("Error in serializing time string")

    return time

def get_launch_details(id):
    description = ""
    image = ""
    requestData = requests.get('https://launchlibrary.net/1.4/launch/'+str(id), auth=('user', 'pass'))

    if requestData.status_code == 200:
        requestData = requestData.json()
        if "launches" in requestData:
            for launch in requestData["launches"]:

                try:
                    if "missions" in launch and not description:
                        description = launch["missions"][0]["description"]

                    if not image and "rocket" in launch:
                        if "imageURL" in launch["rocket"]:
                            if not "placeholder" in launch["rocket"]["imageURL"]:
                                if launch["rocket"]["imageURL"].split(".")[-1].replace("/","") in ["jpg","png","jpeg","gif"]:
                                    image = launch["rocket"]["imageURL"]

                except: pass

    return description, image

def get_launches():
    launches = []
    requestData = requests.get('https://launchlibrary.net/1.4/launch', auth=('user', 'pass'))

    if requestData.status_code == 200:
        requestData = requestData.json()

        for launch in requestData["launches"]:
            launchData = {"posted":False}
            launchData["name"] = launch["name"]
            launchData["time_raw"] = launch["net"]
            launchData["time"] = serializeTime(launch["net"])
            launchData["info"] = launchInfoUrls = []
            launchData["videos"] = launchVidUrls = []
            launchData["description"], launchData["image"] = get_launch_details(launch["id"])

            if "infoURLs" in launch:
                launchData["info"] = launch["infoURLs"]
            if "vidURLs" in launch:
                launchData["videos"] = launch["vidURLs"]

            if launchData["time"]:
                launches.append(launchData)

    return launches

def write_launches():
    with open("launches.json","w") as launchData:
        launchData.write(json.dumps(get_launches(),indent=4))


write_launches()