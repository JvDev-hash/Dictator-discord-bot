import random
import asyncio
import aiohttp
import json
from discord import Game
from discord.ext.commands import Bot
from discord.ext import commands as cmds
from discord import ChannelType
from discord import Channel
import numpy as np
import subprocess as sb
import discord

BOT_PREFIX = ("-")
TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'  # Get at discordapp.com/developers/applications/me

client = Bot(command_prefix=BOT_PREFIX)
client.remove_command('help')

# Command -dt = Insert the chosen channel and the tags chosen to him, because the verification will compare this tags on this and other channels        
@client.command(name='dt',
                description="Insert the chosen channel and the tags chosen to him",
                pass_context=True)
async def insert(context, *args):
    actualServer = context.message.server.name
    arrayTags = list(args)
    littleChannel = arrayTags[0]
    arrayTags.pop(0)
    mydict = {}
    keys = len(arrayTags)
    for i in range(keys):

        tag = "tag"+str(i)
        mydict[tag] = arrayTags[i]
        
    mydict["channel"] = littleChannel

    archiveName = actualServer + "-" + str(littleChannel) + ".json"
    with open(archiveName, 'w') as fp:
        json.dump(mydict, fp)

    sb.call("./permit.sh")
    await client.send_message(context.message.channel, "Oookay hooman {0.author.mention}, am doin a sniff snoff in this bork letters place for you :dog2: ".format(context.message))

# Command -dr = Remove an channel and tags associated to him, from the eyes of the bot
@client.command(name='dr',
                description="Remove an channel and tags associated to him, from the eyes of the bot",
                pass_context=True)
async def remover(context, canal):
    actualServer = context.message.server.name
    argument = actualServer + "-" + canal + ".json"
    sb.call(["./remove.sh", argument])
    await client.send_message(context.message.channel, "Sniff.. Oookay hooman.. am doin a leave that bork letters place :dog2: :cry:")

# Command -dh = List of commands aka Help command
@client.command(name='dh',
                description="Custom Help command",
                pass_context=True)
async def halper(context):
    author = context.message.author

    embed = discord.Embed(
        colour = discord.Colour.orange()
    )

    embed.set_author(name = '[Doggo Halp]')

    url = 'https://gist.githubusercontent.com/JvDev-hash/7b08167ea5c794dc6a0767169c4dd86d/raw/805df9e2d53da07256a15201deda729dce38ec5c/commands_doggo.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)

    keys = len(response["commands"])
    for i in range(keys):

        tag = "tag"+str(i)
        embed.add_field(name = str(response["commands"][tag])[0:3], value = str(response["commands"][tag])[6:], inline = False)

    await client.send_message(context.message.channel, " :dog: Bork!! Oookay hooman, am doin a send the list of my tricks.. :dog2: ".format(context.message))
    await client.send_message(author, embed=embed)

@client.event
async def on_message(message):

    # 'PrivateChannel' object has no attribute 'server'
    if message.channel.type == ChannelType.private:
        return

    founded = "No"

    # Getting the actual server and all channels on him
    actualServer = message.channel.server
    todos_canal = []
    i = 0
    for canal in actualServer.channels:
        if canal.type == ChannelType.text:
            todos_canal.insert(i, canal.id)
            i = i + 1
            
    # We do not want the bot to reply to itself
    if message.author == client.user:
        return
    
    # If the message is a command, process as a command
    if message.content.startswith("-d"):
        await client.process_commands(message)

    else:
        try:
            # Verification if the message contains a blacklisted word in this channel, and moving her to the right place
            for canal in actualServer.channels:
                if canal.type == ChannelType.text:
                    jsonName = actualServer.name + "-" + str(canal.name) + ".json"
                    outputChannels = sb.check_output(["./list.sh", actualServer.name]).decode("utf-8").split("\n")
                    outputChannels.remove("")
                    if jsonName in outputChannels and founded != "Yes":
                        with open(jsonName, 'r') as f:
                            open_dict = json.load(f)
                            idTags = len(open_dict) - 1
                            for i in range(idTags):
                                newTags = "tag"+str(i)
                                dictValue = open_dict.get(newTags)
                                if dictValue.upper() in message.content.upper() and message.channel.name != open_dict.get("channel"):
                                    msg = "AWOOOOO! :dog: Hey fren {0.author.mention}, your bork doesn't belongs here: {0.channel}".format(message)
                                    sending = "Bork! :dog: The hooman {0.author.mention} borked this on wrong place".format(message)
                                    founded = "Yes"
                                    
                                    await client.send_message(message.channel, msg)
                                    await client.delete_message(message)
                                    await client.send_message(client.get_channel(canal.id), sending)
                                    await client.send_message(client.get_channel(canal.id), message.content)
                                    

                                    break

                                else:
                                    pass

                if founded == "Yes":
                    break
                else:
                    continue

        except sb.CalledProcessError:
            return
    

@client.event
async def on_ready():
    print("Logged in as " + client.user.name)

async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)

# Looping to change the status
async def status_task():
    await client.wait_until_ready()
    while True:
        await client.change_presence(game=Game(name="For my tricks, bork -dh", type=0))
        await asyncio.sleep(50)
        await client.change_presence(game=Game(name="Doin a sniff snoff on hoomans", type=0))
        await asyncio.sleep(50)

client.loop.create_task(list_servers())
client.loop.create_task(status_task())
client.run(TOKEN)
