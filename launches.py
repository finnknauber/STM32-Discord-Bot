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
    get_launches()

    channel = client.get_channel(741002663650525245)
    await channel.send("test")
