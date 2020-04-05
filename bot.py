# bot.py
import os
import discord

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client()
@client.event
async def on_ready():
    print('Connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content[0] == "*":
        if 'test' in message.content:
            await message.channel.send("I am up and running!")
        elif 'commands' in message.content:
            await message.channel.send("?bootloader/?hid, ?f4, ?resistor, ?r3, ?r10")
        elif 'help' in message.content:
            await message.channel.send("No")
        elif 'give caleb money' in message.content:
            await message.channel.send("Why? anyways I guess here you go: https://www.patreon.com/user?u=7985126")
        elif 'bootloader' in message.content or 'hid' in message.content:
            await message.channel.send("Take a look here: https://www.youtube.com/watch?v=Myon8H111PQ")
        elif 'f4' in message.content or 'F4' in message.content:
            await message.channel.send("Take a look here: https://www.youtube.com/watch?v=b1123kz_3MM")
        elif 'resistor' in message.content or 'res' in message.content:
            await message.channel.send("There are two known resistor issues. For more info type ?R3 or ?R10")
        elif 'R3' in message.content or 'r3' in message.content:
            await message.channel.send("Some blue pills have a wrong resistor at R3. Sometimes it is close to 100k when it should be around 10k. The high value causes a voltage drop, which results in about 0.8V at the BOOT0 pin on the chip. This voltage is not high enough to be recognized as a logic high. This means the board will not enter the bootmode. Potential fix: desolder the resistor and solder a new one with a value close to 10k. Example:")
            await message.channel.send(file=discord.File('R3.png'))
        elif 'R10' in message.content or 'r10' in message.content:
            await message.channel.send("Some blue pills have a wrong resistor at R10. This resistor is used for USB communication and it should be 1.5k. If you want to use USB-communication you will need to replace it. First desolder the old R10 resistor and make sure the two pads are not connected. Next you have two options: Solder a 1.5k resistor directly to the pads (difficult/not recommended) or solder a resistor from a 3.3V pin to A12.")
        elif 'thank you' in message.content or 'Thank you' in message.content:
            await message.channel.send("No Problem!")

client.run(TOKEN)