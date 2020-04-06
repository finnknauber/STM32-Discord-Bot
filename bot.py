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
    await message.channel.send(image)

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

def userHasEntrywithResult(author, data):
    if getOldEntry(author, data)["result"] == None:
        return False
    else:
        return True


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

def removeJson(key, jsonObject, data):
    data[key].remove(jsonObject)
    writeJson(data)

async def addResult(data, message):
    editJson("lastadds", data, getOldEntry(message.author.name, data), "result", message.content)
    await sendText(message, 'Enter an imgur link, or type "null"')

async def finishAdding(data, message):
    jsonObject = getOldEntry(message.author.name, data)
    removeJson("lastadds", jsonObject, data)
    del jsonObject["user"]
    if not message.content.lower() == "null":
        await sendText(message, 'Command is ready to be used!')
        jsonObject["image"] = message.content
    else:
        await sendText(message, 'Image added and command is ready to be used!')
        jsonObject["image"] = None
    addJson("commands", jsonObject, data)

def getCommandEntry(command,data):
    for entry in data["commands"]:
        if command in entry["command"]:
            return entry
    return None

async def commandAdd(message, names, data):
    if len(names) != 0:
        jsonObject = {"user": message.author.name, "command": names, "result": None}
        addJson("lastadds", jsonObject, data)
        await sendText(message, f"Type your response for {'/'.join(names)} next!")
    else:
        await sendText(message, "No names found, please try again or type $help")

async def commandRemove(message, commandName, data):
    if len(commandName) != 0:
        entry = getCommandEntry(commandName[0], data)
        if entry:
            removeJson("commands", entry, data)
            await sendText(message, f"Removed {commandName[0]}!")
        else:
            await sendText(message, f"Command '{commandName[0]}' was not found!")
    else:
        await sendText(message, "Please type a command name or $help")

async def commandEdit(message, command, data):
    if len(command) >= 3:
        entry = getCommandEntry(command[0], data)
        if command[1] == "name":
            editJson("commands", data, entry, "command", command[2:])
            await sendText(message, f"Succesfully changed command to '{'/'.join(command[2:])}'")
        elif command[1] == "response":
            editJson("commands", data, entry, "result", ' '.join(command[2:]))
            await sendText(message, f"Succesfully changed the response to '{' '.join(command[2:])}'")
        elif command[1] == "image":
            if command[2].lower() == "null":
                editJson("commands", data, entry, "image", None)
            else:
                editJson("commands", data, entry, "image", command[2])
            await sendText(message, f"Succesfully changed the image url to '{command[2]}'")
        else:
            await sendText(message, "Please specify what parameter you want to edit or type $help")
    else:
        await sendText(message, "Please enter all required parameters or type $help")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if len(message.content) > 0:

        with open("./commands.json") as commands:
            data = json.load(commands)

        if message.content[0] == "$":
            
            if userIsEditing(message.author.name, data):
                jsonObject = getOldEntry(message.author.name, data)
                removeJson("lastadds", jsonObject, data)

            command = message.content[1:]
            commandSplit = command.split(" ")

            if command == "help":
                with open("./README.md") as helpMessage:
                    await sendText(message, helpMessage.read())

            else:
                if hasValidRole(message.author.roles, data["roles"]):

                    if commandSplit[0] == "commandadd":
                        await commandAdd(message, commandSplit[1:], data)
                    elif commandSplit[0] == "commandedit":
                        await commandEdit(message, commandSplit[1:], data)
                    elif commandSplit[0] == "commandremove":
                        await commandRemove(message, commandSplit[1:], data)
                    else:
                        await executeCommand(message, data, command)

                else:
                    await executeCommand(message, data, command)

        elif userIsEditing(message.author.name, data):
            if not userHasEntrywithResult(message.author.name, data):
                await addResult(data, message)
            else:
                await finishAdding(data, message)


client.run(TOKEN)