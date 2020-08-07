#!print_launches.py
import os
import json
import datetime
import discord

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client()

message = ""

@client.event
async def on_ready():
    global message
    print("Sending Message")
    channel = client.get_channel(741002663650525245)
    if channel:
        await channel.send(message)
    await client.close()

def getJson():
    global message
    if os.path.exists("launches.json"):
        with open("launches.json") as launchData:
            launchData = json.loads(launchData.read())
            now = datetime.datetime.utcnow()

            for launch in launchData:
                if not launch["posted"]:
                    
                    launchTime = datetime.datetime(day=launch["time"]["day"],
                                            month=launch["time"]["month"],
                                            year=launch["time"]["year"],
                                            hour=launch["time"]["hour"],
                                            minute=launch["time"]["minute"],
                                            second=launch["time"]["second"])
                    before = launchTime - datetime.timedelta(minutes=15)
                    
                    if now >= before and now < launchTime:
                        launch["posted"] = True

                        message = "**Launching '" + launch["name"] + "'** in 15 Minutes\n"
                        message += "**Time:** " + launch["time_raw"] + "\n"
                        if launch["description"]:
                            message += "**Info**: " + launch["description"] + "\n\n"

                        for video in launch["videos"]:
                            message += "*Watch here:* <" + video + ">\n"
                        if not launch["videos"]:
                            message += "*No livestream available*\n"
                            
                        if launch["info"]:
                            for info in launch["info"]:
                                message += "*More info:* <" + info + ">\n"
                                
                        if launch["image"]:
                            message += launch["image"]

        with open("launches.json","w") as launchFile:
            launchFile.write(json.dumps(launchData,indent=4))

getJson()
if message:
    client.run(TOKEN)

