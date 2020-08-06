# launches.py
import os
import requests
import discord

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client()

@client.event
async def on_ready():
    print("test")
    channel = client.get_channel(741002663650525245)
    if channel:
        await channel.send("test")

client.run(TOKEN)

client.logout()
