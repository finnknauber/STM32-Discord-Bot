#!print_launches.py
import os
import json
import datetime
import discord
import get_launches

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


def get_first_launch(launch_data):
    if "results" in launch_data:
        for result in launch_data["results"]:
            if result["status"]["name"] != "Success":
                return result    
    else:
        return {}


def get_launch(launch_data):
    launch = ""
    if launch_data != "":
        launch_string="**" + launch["name"] + "**"

        if "lsp_name" in launch_data:
            launch_string+=" by *" + launch_data["lsp_name"] + "*"
        
        launch_string+=" is launching on " + launch_data["net"]

        if "launcher" in launch_data:
            if launch_data["launcher"]:
                launch_string+=" using **" + launch_data["launcher"] + "**"

        if "pad" in launch_data:
            launch_string+=" from **" + launch_data["pad"] + "**"
            launch_string+=" in **" + launch_data["location"] + "**"
        
        if "landing" in launch_data:
            if launch_data["landing"]:
                launch_string+=" a landing will be attempted on/at **" + launch_data["landing"] + "**"

        launch_string+=". \nThe current mission status is **" + launch_data["status"]["name"] + "**"

        if "mission_type" in launch_data:
            launch_string+="\nThe missions purpose is **" + launch_data["mission_type"] + "**"

        if "orbit" in launch_data:
            if launch_data["orbit"]:
                launch_string+=".\nIt is headed to **" + launch_data["orbit"] + "**"

        if "infographic" in launch_data:
            if launch_data["infographic"]:
                launch_string+="\n"+launch_data["infographic"]
            elif "image" in launch_data:
                if launch_data["image"]:
                    launch_string+="\n"+launch_data["image"]

        elif "image" in launch_data:
            if launch_data["image"]:
                launch_string+="\n"+launch_data["image"]

        launches+=launch_string + "\n\n"

    return launch


message = get_launch(get_first_launch(get_launches.get_file_json()))

if message:
    client.run(TOKEN)
