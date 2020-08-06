# launches.py
import os
import requests
import discord

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client()

message =""

@client.event
async def on_ready():
    print("Sending Message")
    channel = client.get_channel(741002663650525245)
    if channel:
        await channel.send(message)
    await client.close()

def getJson():
    message = "Next rocket launch"

getJson()
if message:
    client.run(TOKEN)

