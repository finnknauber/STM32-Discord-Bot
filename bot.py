# bot.py
import os
import discord
import json

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client()
@client.event
async def on_ready():
    print('Connected to Discord!')

def hasValidRole(roles, validRoles):
    for role in roles:
        if role.name in validRoles:
            return True
    return False

async def sendText(message, text):
    await message.channel.send(text)

async def sendImage(message, image):
    await message.channel.send(file=discord.File(image))

async def executeCommand(message, data, command):
    for command_object in data["commands"]:
        for command_name in command_object["command"]:
            if command_name == command:
                await sendText(message, command_object["result"])
                if command_object["image"]:
                    await sendImage(message, command_object["image"])

def userIsEditing(author,data):
    if getOldEntry(author, data):
        return True
    return False

def getOldEntry(author,data):
    for edit in data["lastadds"]:
        if author == edit["user"]:
            return edit
    return None

def writeJson(data):
    with open("./commands.json", "w") as commands:
        jsonString = json.dumps(data, indent=4)
        commands.write(jsonString)


def addJson(key, jsonObject, data):
    data[key].append(jsonObject)
    writeJson(data)

def editJson(key, data, oldEntry, entryKey, value):
    for entry in data[key]:
        if entry == oldEntry:
            entry[entryKey] = value 
    writeJson(data)



async def commandAdd(message, names, data):
    if len(names) != 0:
        jsonObject = {"user": message.author.name, "command": names, "result": None}
        addJson("lastadds", jsonObject, data)
    else:
        await sendText(message, "No names found, please try again")



@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if len(message.content) > 0:

        with open("./commands.json") as commands:
            data = json.load(commands)

        if message.content[0] == "$":

            command = message.content[1:]
            commandSplit = command.split(" ")

            if hasValidRole(message.author.roles, data["roles"]):

                if commandSplit[0] == "commandadd":
                    await commandAdd(message, commandSplit[1:], data)
                elif commandSplit[0] == "commandedit":
                    pass
                elif commandSplit[0] == "commandremove":
                    pass
                elif commandSplit[0] == "roleadd":
                    pass
                elif commandSplit[0] == "roleremove":
                    pass
                else:
                    await executeCommand(message, data, command)

            else:
                await executeCommand(message, data, command)

        elif userIsEditing(message.author.name, data):
            editJson("lastadds", data, getOldEntry(message.author.name, data), "result", message.content)



client.run(TOKEN)






"""
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
            """